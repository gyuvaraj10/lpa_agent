from typing import Literal

from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

from state.graph_state import GraphState

# FCombine policy and fraud results into a final outcome
# Input: Policy results, fraud flags, credit data
# Output: Decision (Approve, Refer to underwriter or Decline), recorded with rationale
# {"decision":"refer","reason_codes":["INCOME_DISCREPANCY"],"rationale":"Policy passed, but stated income exceeds verified deposits by 28%."}

class DecisionResult(BaseModel):
    decision: Literal["approve","refer","decline"]
    reason_codes: list[str]
    rationale: str
    tools_consulted: list[str]

class DecisionAgent:

    failure_mode = None
    def __init__(self, model, failure_mode: str) -> None:
        self.model = model
        DecisionAgent.failure_mode = failure_mode
        self.system_prompt = f"""
        You are the decision agent. Choose approve, refer or decline using only the policy, fraud and credit results provided. Never approve if the policy verdict is fail or fraud severity is high. Refer if the verdict is borderline, fraud severity is medium, or data is insufficient. Never use name, gender, age or other protected attributes. Cite only facts present in the inputs. Then call decision_writer.
        """

    @tool(description='Write decision') 
    @staticmethod   
    def decision_writer(applicant_id):
        return {}

    # LLM reasoning, tool
    def check_fraud(self, state: GraphState):
        agent = create_agent(system_prompt=self.system_prompt, 
                                model=self.model,
                                middleware=[],
                                name="decision_agent",
                                tools=[DecisionAgent.decision_writer])
        response = agent.invoke({'messages': [{
            'role': 'user',
            'content': f"""
                """
            }]
        })
        return {'final_decision': response['structured_response'] }
