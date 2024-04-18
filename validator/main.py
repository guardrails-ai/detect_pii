import json
from typing import Any, Callable, Dict, List, Union, cast

import nltk
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


@register_validator(name="guardrails/detect_pii", data_type="string")
class DetectPII(Validator):
    """Validates that any text does not contain any PII.

    This validator uses Microsoft's Presidio (https://github.com/microsoft/presidio)
    to detect PII in the text. If PII is detected, the validator will fail with a
    programmatic fix that anonymizes the text. Otherwise, the validator will pass.

    **Key Properties**

    | Property                      | Description                             |
    | ----------------------------- | --------------------------------------- |
    | Name for `format` attribute   | `pii`                                   |
    | Supported data types          | `string`                                |
    | Programmatic fix              | Anonymized text with PII filtered out   |

    Args:
        pii_entities (str | List[str], optional): The PII entities to filter. Must be
            one of `pii` or `spi`. Defaults to None. Can also be set in metadata.
    """

    PII_ENTITIES_MAP = {
        "pii": [
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "DOMAIN_NAME",
            "IP_ADDRESS",
            "DATE_TIME",
            "LOCATION",
            "PERSON",
            "URL",
        ],
        "spi": [
            "CREDIT_CARD",
            "CRYPTO",
            "IBAN_CODE",
            "NRP",
            "MEDICAL_LICENSE",
            "US_BANK_NUMBER",
            "US_DRIVER_LICENSE",
            "US_ITIN",
            "US_PASSPORT",
            "US_SSN",
        ],
    }

    def __init__(
        self,
        pii_entities: Union[str, List[str], None] = None,
        on_fail: Union[Callable[..., Any], None] = None,
        **kwargs,
    ):
        super().__init__(on_fail, pii_entities=pii_entities, **kwargs)
        self.pii_entities = pii_entities
        self.pii_analyzer = AnalyzerEngine()
        self.pii_anonymizer = AnonymizerEngine()

    def get_anonymized_text(self, text: str, entities: List[str]) -> str:
        """Analyze and anonymize the text for PII.

        Args:
            text (str): The text to analyze.
            pii_entities (List[str]): The PII entities to filter.

        Returns:
            anonymized_text (str): The anonymized text.
        """
        results = self.pii_analyzer.analyze(text=text, entities=entities, language="en")
        results = cast(List[Any], results)
        anonymized_text = self.pii_anonymizer.anonymize(
            text=text, analyzer_results=results
        ).text
        return anonymized_text

    def validate(self, value: Any, metadata: Dict[str, Any]) -> ValidationResult:
        # Entities to filter passed through metadata take precedence
        pii_entities = metadata.get("pii_entities", self.pii_entities)
        if pii_entities is None:
            raise ValueError(
                "`pii_entities` must be set in order to use the `DetectPII` validator."
                "Add this: `pii_entities=['PERSON', 'PHONE_NUMBER']`"
                "OR pii_entities='pii' or 'spi'"
                "in init or metadata."
            )

        pii_keys = list(self.PII_ENTITIES_MAP.keys())
        # Check that pii_entities is a string OR list of strings
        if isinstance(pii_entities, str):
            # A key to the PII_ENTITIES_MAP
            entities_to_filter = self.PII_ENTITIES_MAP.get(pii_entities, None)
            if entities_to_filter is None:
                raise ValueError(f"`pii_entities` must be one of {pii_keys}")
        elif isinstance(pii_entities, list):
            entities_to_filter = pii_entities
        else:
            raise ValueError(
                f"`pii_entities` must be one of {pii_keys}" " or a list of strings."
            )

        # split value into just the most recent string
        most_recent_sentence = nltk.sent_tokenize(value)[-1]

        # Analyze the text, and anonymize it if there is PII
        anonymized_text = self.get_anonymized_text(
            text=most_recent_sentence, entities=entities_to_filter
        )

        # If anonymized value text is different from original value, then there is PII
        if anonymized_text != most_recent_sentence:
            anon_split = anonymized_text.split(" ")
            normal_split = most_recent_sentence.split(" ")
            filtered_recent_sentence = most_recent_sentence
            # for i in range(len(anonymized_text.split(" "))):
            #     anonymized = anonymized_text[i]
            #     normal = most_recent_sentence[i]
            #     if anonymized != normal
            anon = 0
            normal = 0

            sensitive_tokens = []
            while anon < len(anon_split):
                if anon_split[anon] == normal_split[normal]:
                    anon += 1
                    normal += 1
                    continue
                else:
                    anon += 1
                    collect = []
                    if anon >= len(anon_split):
                        collect = normal_split[normal:]
                    else:
                        next_word = anon_split[anon]
                        while normal_split[normal] != next_word:
                            collect.append(normal_split[normal])
                            normal += 1
                    collect = " ".join(collect)
                    sensitive_tokens.append(collect)

            return FailResult(
                metadata=metadata,
                violation="DetectPII",
                fix_value=None,
                error_message=json.dumps(
                    {
                        "match_string": sensitive_tokens,
                        "violation": "DetectPII",
                        "error_msg": "This text contains PII",
                        "fix_value": None,
                    },
                ),
            )
        return PassResult()
