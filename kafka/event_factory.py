
import uuid
from datetime import datetime


def create_event(
    event_type,
    user_id,
    source,
    payload
):

    return {
        "event_id": "EVT-" + uuid.uuid4().hex[:12].upper(),
        "event_type": event_type,
        "user_id": user_id,
        "source": source,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }


def create_identity_verification_event(
    user_id,
    verification_score,
    decision
):

    return create_event(
        "identity.verification.completed",
        user_id,
        "identity_verification_pipeline",
        {
            "verification_score": verification_score,
            "decision": decision
        }
    )


def create_fraud_signal_event(
    user_id,
    signal_type,
    severity,
    score
):

    return create_event(
        "fraud.signal.detected",
        user_id,
        "fraud_intelligence",
        {
            "signal_type": signal_type,
            "severity": severity,
            "score": score
        }
    )


def create_trust_score_event(
    user_id,
    trust_score,
    risk_level
):

    return create_event(
        "trust.score.calculated",
        user_id,
        "trust_scoring",
        {
            "trust_score": trust_score,
            "risk_level": risk_level
        }
    )
