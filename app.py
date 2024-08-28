from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

app = FastAPI()

class DetectPII:
    model_name = "presidio-pii"
    validation_method = "sentence"

    def __init__(self):
        self.pii_analyzer = AnalyzerEngine()
        self.pii_anonymizer = AnonymizerEngine()

    def infer(self, text_vals: List[str], entities: List[str]) -> OutputResponse:
        outputs = []
        for idx, text in enumerate(text_vals):
            anonymized_text = self.get_anonymized_text(text, entities)
            results = anonymized_text if anonymized_text != text else text

            outputs.append(
                InferenceData(
                    name=f"result{idx}",
                    datatype="BYTES",
                    shape=[len(results)],
                    data=[results],
                )
            )

        return OutputResponse(
            modelname=DetectPII.model_name,
            modelversion="1",
            outputs=outputs
        )

    def get_anonymized_text(self, text: str, entities: List[str]) -> str:
        results = self.pii_analyzer.analyze(text=text, entities=entities, language="en")
        anonymized_text = self.pii_anonymizer.anonymize(
            text=text, analyzer_results=results
        ).text
        return anonymized_text

pii_service = DetectPII()
# Define PII entities map
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

class InferenceData(BaseModel):
    name: str
    shape: List[int]
    data: List
    datatype: str

class InputRequest(BaseModel):
    inputs: List[InferenceData]

class OutputResponse(BaseModel):
    modelname: str
    modelversion: str
    outputs: List[InferenceData]

@app.get("/")
async def hello_world():
    return "detect-pii"

@app.post("/validate", response_model=OutputResponse)
async def check_pii(input_request: InputRequest):
    text_vals = None
    pii_entities = None

    for inp in input_request.inputs:
        if inp.name == "text":
            text_vals = inp.data
        elif inp.name == "pii_entities":
            pii_entities = inp.data

    if text_vals is None or pii_entities is None:
        raise HTTPException(status_code=400, detail="Invalid input format")

    if isinstance(pii_entities, str):
        entities_to_filter = PII_ENTITIES_MAP.get(pii_entities)
        if entities_to_filter is None:
            raise HTTPException(status_code=400, detail="Invalid PII entity type")
    elif isinstance(pii_entities, list):
        entities_to_filter = pii_entities
    else:
        raise HTTPException(status_code=400, detail="Invalid PII entity format")
    return pii_service.infer(text_vals, entities_to_filter)

# Run the app with uvicorn
# Save this script as app.py and run with: uvicorn app:app --reload
