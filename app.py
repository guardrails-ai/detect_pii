from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

app = FastAPI()

# Initialize the Presidio Analyzer and Anonymizer engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

class InferenceData(BaseModel):
    name: str
    shape: List[int]
    data: Union[List[str], List[float]]
    datatype: str

class InputRequest(BaseModel):
    inputs: List[InferenceData]

class OutputResponse(BaseModel):
    modelname: str
    modelversion: str
    outputs: List[InferenceData]

@app.post("/validate", response_model=OutputResponse)
async def detect_pii(input_request: InputRequest):
    text = None
    entities = None
    
    for inp in input_request.inputs:
        if inp.name == "text":
            text = inp.data[0]
        elif inp.name == "entities":
            entities = inp.data
    
    if text is None or entities is None:
        raise HTTPException(status_code=400, detail="Invalid input format")

    # Analyze the text to detect PII and anonymize it
    if isinstance(entities, str):
        entities = [entities]
    results = analyzer.analyze(text=text, entities=entities, language="en")
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results).text
    
    output_data = OutputResponse(
        modelname="DetectPIIModel",
        modelversion="1",
        outputs=[
            InferenceData(
                name="result",
                datatype="BYTES",
                shape=[1],
                data=[anonymized_text]
            )
        ]
    )
    
    print(f"Output data: {output_data}")
    return output_data

# Run the app with uvicorn
# Save this script as app.py and run with: uvicorn app:app --reload
