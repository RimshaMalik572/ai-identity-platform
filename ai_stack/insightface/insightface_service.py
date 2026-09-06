
import insightface


class InsightFaceService:

    def __init__(self):

        self.app = None
        self.initialized = False

    def initialize(self):

        try:

            self.app = insightface.app.FaceAnalysis(
                name="buffalo_l"
            )

            self.app.prepare(
                ctx_id=0,
                det_size=(640, 640)
            )

            self.initialized = True

            return {
                "status": "initialized",
                "model": "buffalo_l"
            }

        except Exception as e:

            return {
                "status": "initialization_failed",
                "reason": str(e)
            }

    def analyze(self, image):

        if not self.initialized:

            result = self.initialize()

            if result["status"] != "initialized":
                return result

        faces = self.app.get(image)

        return {
            "status": "success",
            "face_count": len(faces),
            "faces": [
                {
                    "bbox": face.bbox.tolist(),
                    "det_score": float(face.det_score),
                    "embedding_dimension": (
                        len(face.embedding)
                        if face.embedding is not None
                        else 0
                    )
                }
                for face in faces
            ]
        }
