from typing import TypedDict


class GraphState(TypedDict):
    document_info: dict
    credit_into: dict
    compliance_info: dict
    fraud_info: dict