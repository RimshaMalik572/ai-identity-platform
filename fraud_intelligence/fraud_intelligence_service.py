
from typing import Dict, Any, List


class FraudIntelligenceService:

    def __init__(self):
        self.name = "Fraud Intelligence Layer"

    def analyze(self, evidence: Dict[str, Any]) -> Dict[str, Any]:

        signals = evidence.get("signals", {})

        indicators: List[Dict[str, Any]] = []

        # ----------------------------------------
        # Deepfake signal
        # ----------------------------------------
        deepfake_probability = signals.get(
            "deepfake_probability",
            0.0
        )

        if deepfake_probability >= 70:
            indicators.append({
                "type": "deepfake_risk",
                "severity": "HIGH",
                "value": deepfake_probability,
                "description": "Elevated deepfake probability detected"
            })

        # ----------------------------------------
        # Identity verification
        # ----------------------------------------
        identity_score = signals.get(
            "identity_verification_score",
            0.0
        )

        if identity_score < 70:
            indicators.append({
                "type": "identity_risk",
                "severity": "HIGH",
                "value": identity_score,
                "description": "Identity verification score below threshold"
            })

        # ----------------------------------------
        # Voice authentication
        # ----------------------------------------
        voice_score = signals.get(
            "voice_score",
            0.0
        )

        if 0 < voice_score < 60:
            indicators.append({
                "type": "voice_risk",
                "severity": "MEDIUM",
                "value": voice_score,
                "description": "Voice authentication score requires attention"
            })

        # ----------------------------------------
        # Document intelligence
        # ----------------------------------------
        document_score = signals.get(
            "document_score",
            0.0
        )

        if 0 < document_score < 60:
            indicators.append({
                "type": "document_risk",
                "severity": "MEDIUM",
                "value": document_score,
                "description": "Document intelligence score requires attention"
            })

        # ----------------------------------------
        # Behavioral biometrics
        # ----------------------------------------
        behavioral_score = signals.get(
            "behavioral_score",
            0.0
        )

        if 0 < behavioral_score < 60:
            indicators.append({
                "type": "behavioral_risk",
                "severity": "MEDIUM",
                "value": behavioral_score,
                "description": "Behavioral anomaly detected"
            })

        # ----------------------------------------
        # Device intelligence
        # ----------------------------------------
        device_score = signals.get(
            "device_score",
            0.0
        )

        if 0 < device_score < 60:
            indicators.append({
                "type": "device_risk",
                "severity": "MEDIUM",
                "value": device_score,
                "description": "Device intelligence score requires attention"
            })

        # ----------------------------------------
        # Historical activity
        # ----------------------------------------
        historical_score = signals.get(
            "historical_score",
            0.0
        )

        if 0 < historical_score < 60:
            indicators.append({
                "type": "historical_risk",
                "severity": "MEDIUM",
                "value": historical_score,
                "description": "Historical activity indicates elevated risk"
            })

        # ----------------------------------------
        # Geo-location
        # ----------------------------------------
        geo_score = signals.get(
            "geo_score",
            0.0
        )

        if 0 < geo_score < 60:
            indicators.append({
                "type": "geo_risk",
                "severity": "MEDIUM",
                "value": geo_score,
                "description": "Geographic signal requires attention"
            })

        # ----------------------------------------
        # Fraud risk calculation
        # ----------------------------------------

        severity_weight = {
            "HIGH": 1.0,
            "MEDIUM": 0.6,
            "LOW": 0.3
        }

        if indicators:
            fraud_risk = min(
                100.0,
                sum(
                    severity_weight[i["severity"]]
                    * 50
                    for i in indicators
                )
            )
        else:
            fraud_risk = 0.0

        # ----------------------------------------
        # Risk level
        # ----------------------------------------

        if fraud_risk >= 70:
            risk_level = "HIGH"
            action = "MANUAL_REVIEW"
        elif fraud_risk >= 40:
            risk_level = "MEDIUM"
            action = "ADDITIONAL_VERIFICATION"
        else:
            risk_level = "LOW"
            action = "ALLOW_WITH_STANDARD_CONTROLS"

        return {
            "fraud_risk_score": round(fraud_risk, 2),
            "risk_level": risk_level,
            "fraud_indicators": indicators,
            "indicator_count": len(indicators),
            "recommended_action": action
        }
