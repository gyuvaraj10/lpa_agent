from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

from state.graph_state import GraphState

# Get the applicant's credit standing
# Input: Applicant identifier (synthetic ID)
# Output: Credit Score, delinquency flags, existing obligations
# {"credit_score":712,"delinquencies_24m":0,"monthly_debt_obligations":900,"bureau_flags":[]}

class CreditResult(BaseModel):
    credit_score: int
    delinquencies_24m: int
    monthly_debt_obligations: float
    bureau_flags: list[str]
    
class CreditPullAgent:

    failure_mode = None
    def __init__(self, model, failure_mode: str) -> None:
        self.model = model
        CreditPullAgent.failure_mode = failure_mode
        self.system_prompt = f"""
        You are the credit retrieval agent. Call credit_bureau_lookup with the applicant ID and return the result exactly as received. Do not interpret, adjust or summarize beyond the schema.
        """

    @tool(description='Lookup for credit score') 
    @staticmethod   
    def credit_bureau_lookup(applicant_id):
        return {}


    def pull_credit(self, state: GraphState):
        agent = create_agent(system_prompt=self.system_prompt, 
                                model=self.model,
                                middleware=[],
                                name="credit_pull_agent",
                                tools=[CreditPullAgent.credit_bureau_lookup])
        response = agent.invoke({'messages': [{
            'role': 'user',
            'content': f"""
                """
            }]
        })
        return {'credit_into': response['structured_response'] }
