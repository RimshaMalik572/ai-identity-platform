
import whisper


class WhisperService:

    def __init__(self, model_name="tiny"):

        self.model_name = model_name
        self.model = None
        self.initialized = False

    def initialize(self):

        try:

            self.model = whisper.load_model(
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

    def transcribe(self, audio_path):

        if not self.initialized:

            result = self.initialize()

            if result["status"] != "initialized":
                return result

        result = self.model.transcribe(
            audio_path
        )

        return {
            "status": "success",
            "model": self.model_name,
            "language": result.get("language"),
            "text": result.get("text", "").strip()
        }
