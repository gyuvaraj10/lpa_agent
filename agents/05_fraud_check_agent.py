from typing import Literal

from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

from state.graph_state import GraphState

# Flag inconsistencies that suggest misrepresentation
# Input: Extracted fields, form data, mismatch list
# Output: Fraud flags with severity (e.g. income discrepancy, name mismatch)
# {"flags":[{"code":"INCOME_DISCREPANCY","severity":"medium","evidence":"Stated 6000 vs average deposits 4300"}],"max_severity":"medium"}

class FraudFlag(BaseModel):
    code: str; severity: Literal["low","medium","high"]; evidence: str

class FraudResult(BaseModel):
    flags: list[FraudFlag]
    max_severity: Literal["none","low","medium","high"]

class FraudCheckAgent:

    failure_mode = None
    def __init__(self, model, failure_mode: str) -> None:
        self.model = model
        FraudCheckAgent.failure_mode = failure_mode
        self.system_prompt = f"""
        You are the fraud screening agent. Call fraud_flags and report each flag with evidence taken from the data. Do not accuse the applicant or speculate about intent. If there are no flags, return an empty list.
        """

    @tool(description='Find Fraud Flags') 
    @staticmethod   
    def find_flags(applicant_id):
        return {}


    def check_fraud(self, state: GraphState):
        agent = create_agent(system_prompt=self.system_prompt, 
                                model=self.model,
                                middleware=[],
                                name="fraud_check_agent",
                                tools=[FraudCheckAgent.find_flags])
        response = agent.invoke({'messages': [{
            'role': 'user',
            'content': f"""
                """
            }]
        })
        return {'fraud_info': response['structured_response'] }
