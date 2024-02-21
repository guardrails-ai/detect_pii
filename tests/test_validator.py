from guardrails import Guard
from validator import DetectPII


guard = Guard.from_string(validators=[DetectPII(pii_entities="pii", on_fail="fix")])

def test_validator_success():
    TEST_OUTPUT = "My email address is , and my phone number is"
    raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)
    assert guarded_output == TEST_OUTPUT


def test_validator_fail():
  TEST_FAIL_OUTPUT = "My email address is demo@lol.com, and my phone number is 1234567890"
  raw_output, guarded_output, *rest = guard.parse(TEST_FAIL_OUTPUT)
  assert(guarded_output == "My email address is <EMAIL_ADDRESS>, and my phone number is <PHONE_NUMBER>")