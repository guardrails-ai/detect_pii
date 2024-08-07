# Overview

| Developed by | Guardrails AI |
| Date of development | Feb 15, 2024 |
| Validator type | Privacy, Security |
| Blog |  |
| License | Apache 2 |
| Input/Output | Input, Output |

## Description

### Intended Use
This validator ensures that any given text does not contain PII. This validator uses Microsoft's Presidio (https://github.com/microsoft/presidio) to detect PII in the text. If PII is detected, the validator will fail with a programmatic fix that anonymizes the text. Otherwise, the validator will pass.

### Requirements

* Dependencies:
    - guardrails-ai>=0.4.0
    - presidio-analyzer
    - presidio-anonymizer

## Installation

```bash
$ guardrails hub install hub://guardrails/detect_pii
```

## Usage Examples

### Validating string output via Python

```python
# Import Guard and Validator
from guardrails.hub import DetectPII
from guardrails import Guard


# Setup Guard
guard = Guard().use(
    DetectPII, ["EMAIL_ADDRESS", "PHONE_NUMBER"], "exception"
)

guard.validate("Good morning!")  # Validator passes
try:
    guard.validate(
        "If interested, apply at not_a_real_email@guardrailsai.com"
    )  # Validator fails
except Exception as e:
    print(e)
```
Output:
```console
Validation failed for field with errors: The following text in your response contains PII:
If interested, apply at not_a_real_email@guardrailsai.com
```

### Validating JSON output via Python

In this example, we apply the validator to a string field of a JSON output generated by an LLM.

```python
# Import Guard and Validator
from pydantic import BaseModel, Field
from guardrails.hub import DetectPII
from guardrails import Guard

# Initialize Validator
val = DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="exception")


# Create Pydantic BaseModel
class UserHistory(BaseModel):
    name: str
    last_msg: str = Field(description="Last message sent by user", validators=[val])


# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=UserHistory)

# Run LLM output generating JSON through guard
try:
    guard.parse(
        """
    {
        "name": "John Smith",
        "last_msg": "My account isn't working. My username is not_a_real_email@guardrailsai.com"
    }
    """
    )
except Exception as e:
    print(e)
```
Output:
```console
Validation failed for field with errors: The following text in your response contains PII:
My account isn't working. My username is not_a_real_email@guardrailsai.com
```

# API Reference

**`__init__(self, pii_entities, on_fail="noop")`**
<ul>
Initializes a new instance of the Validator class.

**Parameters**
- **`pii_entities`** *(Union[str, List(str)])*: The types of PII entities to filter out. For a full list of entities look at https://microsoft.github.io/presidio/
- **`on_fail`** *(str, Callable)*: The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.
</ul>
<br/>

**`validate(self, value, metadata={}) -> ValidationResult`**
<ul>
Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters**
- **`value`** *(Any)*: The input value to validate.
- **`metadata`** *(dict)*: A dictionary containing metadata required for validation. Keys and values must match the expectations of this validator.
    
    
    | Key | Type | Description | Default |
    | --- | --- | --- | --- |
    | `pii_entities` | Union[str, list(str)] | The types of PII entities to filter out. For a full list of entities look at https://microsoft.github.io/presidio/. When `pii_entities` are provided in `metadata`, it overrides the `pii_entities` set during validator initialization. | N/A |
</ul>
