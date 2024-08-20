from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os

app = FastAPI()

# Initialize the Presidio model once
pii_analyzer = AnalyzerEngine()
pii_anonymizer = AnonymizerEngine()

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

    return DetectPII.infer(text_vals, pii_entities)

class DetectPII:
    model_name = "presidio-pii"
    validation_method = "sentence"

    @staticmethod
    def infer(text_vals: List[str], entities: List[str]) -> OutputResponse:
        outputs = []
        for idx, text in enumerate(text_vals):
            anonymized_text = DetectPII.get_anonymized_text(text, entities)
            results = anonymized_text if anonymized_text != text else []

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

    @staticmethod
    def get_anonymized_text(text: str, entities: List[str]) -> str:
        results = pii_analyzer.analyze(text=text, entities=entities, language="en")
        anonymized_text = pii_anonymizer.anonymize(
            text=text, analyzer_results=results
        ).text
        return anonymized_text

# Run the app with uvicorn
# Save this script as app.py and run with: uvicorn app:app --reload
