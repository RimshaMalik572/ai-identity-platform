
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="AI Identity Platform API",
    description="API Gateway for AI-powered identity verification and fraud intelligence",
    version="1.0.0"
)

# ================================================================
# REQUEST MODELS
# ================================================================

class IdentityVerificationRequest(BaseModel):
    user_id: str
    document_score: Optional[float] = Field(default=None, ge=0, le=100)
    face_similarity: Optional[float] = Field(default=None, ge=-1, le=1)
    deepfake_probability: Optional[float] = Field(default=None, ge=0, le=100)

class FraudSignalRequest(BaseModel):
    user_id: str
    signal_type: str
    severity: str = "MEDIUM"
    score: float = Field(ge=0, le=100)
    description: str

class TrustScoreRequest(BaseModel):
    user_id: str
    signals: Dict[str, float]


# ================================================================
# HEALTH / GATEWAY
# ================================================================

@app.get("/")
def root():
    return {
        "service": "AI Identity Platform",
        "component": "API Gateway",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "api_gateway",
        "timestamp": datetime.utcnow().isoformat()
    }


# ================================================================
# IDENTITY VERIFICATION PIPELINE
# ================================================================

@app.post("/api/v1/identity/verify")
def verify_identity(request: IdentityVerificationRequest):

    verification_id = "VER-" + uuid.uuid4().hex[:10].upper()

    scores = []

    if request.document_score is not None:
        scores.append(request.document_score)

    if request.face_similarity is not None:
        # Convert similarity [-1,1] into approximate percentage
        face_score = max(0, min(100, ((request.face_similarity + 1) / 2) * 100))
        scores.append(face_score)

    if request.deepfake_probability is not None:
        scores.append(100 - request.deepfake_probability)

    final_score = round(sum(scores) / len(scores), 2) if scores else None

    if final_score is None:
        decision = "REVIEW"
    elif final_score >= 80:
        decision = "PASS"
    elif final_score >= 60:
        decision = "REVIEW"
    else:
        decision = "FAIL"

    return {
        "verification_id": verification_id,
        "user_id": request.user_id,
        "pipeline": "identity_verification",
        "verification_score": final_score,
        "decision": decision,
        "timestamp": datetime.utcnow().isoformat()
    }


# ================================================================
# FRAUD INTELLIGENCE LAYER
# ================================================================

@app.post("/api/v1/fraud/signals")
def create_fraud_signal(request: FraudSignalRequest):

    signal_id = "SIG-" + uuid.uuid4().hex[:10].upper()

    return {
        "signal_id": signal_id,
        "user_id": request.user_id,
        "signal_type": request.signal_type,
        "severity": request.severity.upper(),
        "score": request.score,
        "description": request.description,
        "layer": "fraud_intelligence",
        "status": "registered",
        "timestamp": datetime.utcnow().isoformat()
    }


# ================================================================
# TRUST SCORING
# ================================================================

@app.post("/api/v1/trust/score")
def calculate_trust_score(request: TrustScoreRequest):

    if not request.signals:
        raise HTTPException(
            status_code=400,
            detail="At least one trust signal is required"
        )

    score = sum(request.signals.values()) / len(request.signals)
    score = round(max(0, min(100, score)), 2)

    if score >= 80:
        risk = "LOW"
    elif score >= 60:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "user_id": request.user_id,
        "trust_score": score,
        "risk_level": risk,
        "signal_count": len(request.signals),
        "timestamp": datetime.utcnow().isoformat()
    }


# ================================================================
# BIOMETRIC PROCESSING PIPELINE
# ================================================================

@app.get("/api/v1/biometric/status")
def biometric_status():

    return {
        "pipeline": "biometric_processing",
        "status": "ready",
        "components": [
            "face_comparison",
            "deepfake_detection",
            "voice_authentication"
        ]
    }


# ================================================================
# KNOWLEDGE GRAPH
# ================================================================

@app.get("/api/v1/graph/status")
def graph_status():

    return {
        "pipeline": "identity_knowledge_graph",
        "status": "ready",
        "graph_database": "Neo4j",
        "graph_engine": "NetworkX"
    }


# ================================================================
# ALERT CENTER
# ================================================================

@app.get("/api/v1/alerts")
def alerts():

    return {
        "service": "alert_center",
        "status": "ready",
        "supported_alerts": [
            "deepfake_alert",
            "fraud_risk_alert",
            "identity_risk_alert",
            "trust_score_alert",
            "verification_alert",
            "manual_review_alert"
        ]
    }


# ================================================================
# EVENT-DRIVEN ARCHITECTURE
# ================================================================

@app.post("/api/v1/events/publish")
def publish_event(event: Dict[str, Any]):

    event_id = "EVT-" + uuid.uuid4().hex[:10].upper()

    return {
        "event_id": event_id,
        "status": "accepted",
        "event": event,
        "event_bus": "Kafka",
        "timestamp": datetime.utcnow().isoformat()
    }
