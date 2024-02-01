from guardrails import Guard
from pydantic import BaseModel, Field
from validator import PIIFilter


class ValidatorTestObject(BaseModel):
    test_val: str = Field(
        validators=[
            PIIFilter(pii_entities="pii", on_fail="exception")
        ]
    )


TEST_OUTPUT = """
{
  "test_val": "My email address is , and my phone number is"
}
"""


guard = Guard.from_pydantic(output_class=ValidatorTestObject)

raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)

print("validated output: ", guarded_output)


TEST_FAIL_OUTPUT = """
{
"test_val": "My email address is demo@lol.com, and my phone number is 1234567890"
}
"""

try:
  guard.parse(TEST_FAIL_OUTPUT)
  print ("Failed to fail validation when it was supposed to")
except (Exception):
  print ('Successfully failed validation when it was supposed to')