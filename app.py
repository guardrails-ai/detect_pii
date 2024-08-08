from typing import Any, Dict, List, cast


from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class InferlessPythonModel:
    def initialize(self):
        self.pii_analyzer = AnalyzerEngine()
        self.pii_anonymizer = AnonymizerEngine()

    def infer(self, inputs: Dict[str, Any]):
        entities_to_use = inputs["entities"]
        if isinstance(entities_to_use, str):
            entities_to_use = [entities_to_use]
        results = self.pii_analyzer.analyze(
            text=inputs["text"], entities=entities_to_use, language="en"
        )
        results = cast(List[Any], results)
        anonymized_text = self.pii_anonymizer.anonymize(
            text=inputs["text"], analyzer_results=results
        ).text
        return anonymized_text

    def finalize(self):
        pass
