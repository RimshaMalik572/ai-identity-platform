
from paddleocr import PaddleOCR


class PaddleOCRService:

    def __init__(self, language="en"):

        self.language = language
        self.ocr = None
        self.initialized = False

    def initialize(self):

        try:

            self.ocr = PaddleOCR(
                lang=self.language
            )

            self.initialized = True

            return {
                "status": "initialized",
                "language": self.language
            }

        except Exception as e:

            return {
                "status": "initialization_failed",
                "reason": str(e)
            }

    def extract_text(self, image_path):

        if not self.initialized:

            result = self.initialize()

            if result["status"] != "initialized":
                return result

        result = self.ocr.predict(
            image_path
        )

        return {
            "status": "success",
            "result": result
        }
