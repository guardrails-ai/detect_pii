INPUT_SCHEMA = {
    "text": {
        "example": ["My phone number is (555) 555-5555 and my email is test@test.com"],
        "shape": [1],
        "datatype": "STRING",
        "required": True,
    },
    "entities": {
        "example": [
            "PHONE_NUMBER",
            "EMAIL_ADDRESS",
            "DATE_TIME",
            "LOCATION",
            "PERSON",
            "URL",
        ],
        "shape": [-1],
        "datatype": "STRING",
        "required": True,
    },
}
