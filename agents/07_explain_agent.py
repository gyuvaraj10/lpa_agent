from langchain.agents import create_agent
from pydantic import BaseModel

from state.graph_state import GraphState

# Communicate the ourcome clearly and safely
# Input: Decision, rationale, policy results
# Outcome: Customer safe explanation, plus and internal audit note citing the data used.
# {"customer_message":"Thank you for applying. Your application needs a quick review by one of our specialists, who will contact you within 2 business days.","audit_note":"Referred: income discrepancy (stated 6000, deposits avg 4300). Policy pass. Credit 712."}

class ExplanationResult(BaseModel):
    customer_message: str
    audit_note: str
    reason_codes_cited: list[str]

class ExplainAgent:

    def __init__(self) -> None:
        self.model = self.model
        self.system_prompt = f"""
        You are the explanation agent. Write a short, plain-language message for the customer, plus an internal audit note. Use only the decision, reason codes and data provided. Do not mention fraud suspicion, protected attributes or internal scoring thresholds in the customer message. Do not promise outcomes.
        """

    def explain(self, state: GraphState):
        agent = create_agent(system_prompt=self.system_prompt, 
                                model=self.model,
                                middleware=[],
                                name="decision_agent")
        response = agent.invoke({'messages': [{
            'role': 'user',
            'content': f"""
                """
            }]
        })
        return {'final_decision': response['structured_response'] }
