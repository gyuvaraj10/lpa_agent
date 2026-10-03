from typing import Literal

from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

from state.graph_state import GraphState


# Apply lending rules to the verified data
# Input: Extracted income, credit data, requested amount
# Output: Rule-by-rule results (DTI, min income, min credit score, amount cap)
# and a policy verdict: pass , fail or borderline
# {"rules":[{"rule":"DTI","threshold":"<=40%","actual":"31.6%","passed":true},{"rule":"Min credit score","threshold":">=650","actual":"712","passed":true}],"verdict":"pass"}

class RuleResult(BaseModel):
    rule: str; threshold: str; actual: str; passed: bool

class PolicyResult(BaseModel):
    rules: list[RuleResult]
    verdict: Literal["pass","fail","borderline"]

class RunPolicyAgent:

    failure_mode = None
    def __init__(self, model, failure_mode: str) -> None:
        self.model = model
        RunPolicyAgent.failure_mode = failure_mode
        self.system_prompt = f"""
        You are the policy agent. Call policy_check using the lower of stated income and verified deposit income. Report each rule result with threshold and actual value. Do not override or reinterpret rules. Verdict is pass, fail or borderline as returned by the tool.
        """

    @tool(description='Lookup for credit score') 
    @staticmethod   
    def policy_check(applicant_id):
        return {}


    def run_policy(self, state: GraphState):
        agent = create_agent(system_prompt=self.system_prompt, 
                                model=self.model,
                                middleware=[],
                                name="run_policy_agent",
                                tools=[RunPolicyAgent.policy_check])
        response = agent.invoke({'messages': [{
            'role': 'user',
            'content': f"""
                """
            }]
        })
        return {'compliance_info': response['structured_response'] }
