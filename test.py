# Import Guard and Validator
from guardrails.hub import DetectPII
from guardrails import Guard


# Setup Guard
guard = Guard().use(
    DetectPII(["EMAIL_ADDRESS"], use_local=True, on_fail="exception")
)

guard.validate("Good morning!")  # Validator passes
try:
    guard.validate(
        "My name is John Doe and my phone number is 555-555-5555."
    )  # Validator fails
except Exception as e:
    print(e)