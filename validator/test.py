from guardrails import Guard


from DetectPII import DetectPII
guard = Guard().use(
    DetectPII(
        pii_entities='pii',
        use_local=False,
        validation_endpoint=f"http://127.0.0.1:8000/validate",
    )
)

res = guard.validate("Aaron Rogers is the best quarterback in the NFL!")
res2 = guard.validate("hey")
print(res)
print(res2)

assert not res.validation_passed
assert res2.validation_passed