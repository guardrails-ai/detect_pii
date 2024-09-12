import pytest
from validator.main import DetectPII
from guardrails import Guard

# Setup Guard with DetectPII validator
guard = Guard().use(
    DetectPII, ["EMAIL_ADDRESS", "PHONE_NUMBER"], "exception"
)

# Test passing response (no PII)
def test_pii_pass():
    response = guard.validate("My name is John and I love hiking!")
    assert response.validation_passed is True

# Test failing response (contains PII)
def test_pii_fail():
    with pytest.raises(Exception) as e:
        guard.validate(
            "My email address is demo@lol.com, and my phone number is 1234567890"
        )
    assert "Validation failed for field with errors:" in str(e.value)
