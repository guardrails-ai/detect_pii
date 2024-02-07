## Details

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Privacy, Security |
| Blog |  |
| License | Apache 2 |
| Input/Output | Input, Output |

## Description

This validator ensures that any given text does not contain PII. This validator uses Microsoft's Presidio (https://github.com/microsoft/presidio) to detect PII in the text. If PII is detected, the validator will fail with a programmatic fix that anonymizes the text. Otherwise, the validator will pass.

## Example Usage Guide

### Installation

```bash
$ gudardrails hub install PIIFilter
```

### Initialization

```python
pii_validator = PIIFIlter(
	pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"],
	on_fail="fix"
)

guard = Guard.from_string(validators=[pii_validator, ...])
```

### Invocation

```python
guard(
	"Text with PII",
	metadata={"pii_entities": "PHONE_NUMBER"}
)
```

## API Ref

- `pii_entities`: The types of PII entities to filter out. For a full list of entities look at https://microsoft.github.io/presidio/

## Intended use

- Primary intended uses: This is intended to determine if any input or output text has PII.

## Expected deployment metrics

|  | CPU | GPU |
| --- | --- | --- |
| Latency |  | - |
| Memory |  | - |
| Cost |  | - |
| Expected quality |  | - |

## Resources required

- Dependencies: `presidio_analyzer`, `presidio_anonymizer`
- Foundation model access keys: n/a
- Compute: n/a

## Validator Performance

### Evaluation Dataset

-

### Model Performance Measures

| Accuracy |  |
| --- | --- |
| F1 Score |  |

### Decision thresholds

-
