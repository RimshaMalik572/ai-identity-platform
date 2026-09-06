
from ultralytics import YOLO


class YOLOv11Service:

    def __init__(self, model_name="yolo11n.pt"):

        self.model_name = model_name
        self.model = None
        self.initialized = False

    def initialize(self):

        try:

            self.model = YOLO(self.model_name)

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

    def detect(self, image):

        if not self.initialized:

            result = self.initialize()

            if result["status"] != "initialized":
                return result

        results = self.model.predict(
            source=image,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                detections.append({
                    "class_id": int(
                        box.cls[0].item()
                    ),
                    "confidence": float(
                        box.conf[0].item()
                    ),
                    "bbox": [
                        float(x)
                        for x in box.xyxy[0].tolist()
                    ]
                })

        return {
            "status": "success",
            "model": self.model_name,
            "detection_count": len(detections),
            "detections": detections
        }
