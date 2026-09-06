
from transformers import (
    AutoTokenizer,
    AutoModel,
    pipeline
)


class HuggingFaceService:

    def __init__(
        self,
        model_name="distilbert-base-uncased"
    ):

        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self.initialized = False

    def initialize(self):

        try:

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name
            )

            self.model = AutoModel.from_pretrained(
                self.model_name
            )

            self.initialized = True

            return {
                "status": "initialized",
                "model": self.model_name
            }

        except Exception as e:

            return {
                "status": "initialization_failed",
                "reason": str(e)
            }

    def encode(self, text):

        if not self.initialized:

            result = self.initialize()

            if result["status"] != "initialized":
                return result

        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        return {
            "status": "success",
            "input_ids_shape": list(
                encoded["input_ids"].shape
            ),
            "attention_mask_shape": list(
                encoded["attention_mask"].shape
            )
        }

    def classify_text(
        self,
        text,
        model_name="distilbert-base-uncased-finetuned-sst-2-english"
    ):

        try:

            classifier = pipeline(
                "text-classification",
                model=model_name
            )

            result = classifier(text)

            return {
                "status": "success",
                "model": model_name,
                "result": result
            }

        except Exception as e:

            return {
                "status": "classification_failed",
                "reason": str(e)
            }
