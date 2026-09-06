
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class IdentityState(TypedDict, total=False):

    user_id: str
    identity_score: float
    deepfake_probability: float
    trust_score: float
    risk_level: str
    decision: str


def collect_identity_evidence(state):

    return {
        "identity_score": state.get(
            "identity_score",
            0.0
        )
    }


def assess_deepfake_signal(state):

    probability = state.get(
        "deepfake_probability",
        0.0
    )

    return {
        "deepfake_probability": probability
    }


def calculate_risk(state):

    trust_score = state.get(
        "trust_score",
        0.0
    )

    deepfake = state.get(
        "deepfake_probability",
        0.0
    )

    if deepfake >= 70:
        risk = "HIGH"
    elif trust_score < 60:
        risk = "HIGH"
    elif trust_score < 80:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "risk_level": risk
    }


def make_decision(state):

    risk = state.get(
        "risk_level",
        "HIGH"
    )

    identity_score = state.get(
        "identity_score",
        0.0
    )

    if risk == "LOW" and identity_score >= 80:
        decision = "ALLOW"

    elif risk == "HIGH":
        decision = "MANUAL_REVIEW"

    else:
        decision = "REVIEW"

    return {
        "decision": decision
    }


def build_identity_workflow():

    workflow = StateGraph(IdentityState)

    workflow.add_node(
        "collect_identity_evidence",
        collect_identity_evidence
    )

    workflow.add_node(
        "assess_deepfake_signal",
        assess_deepfake_signal
    )

    workflow.add_node(
        "calculate_risk",
        calculate_risk
    )

    workflow.add_node(
        "make_decision",
        make_decision
    )

    workflow.add_edge(
        START,
        "collect_identity_evidence"
    )

    workflow.add_edge(
        "collect_identity_evidence",
        "assess_deepfake_signal"
    )

    workflow.add_edge(
        "assess_deepfake_signal",
        "calculate_risk"
    )

    workflow.add_edge(
        "calculate_risk",
        "make_decision"
    )

    workflow.add_edge(
        "make_decision",
        END
    )

    return workflow.compile()
