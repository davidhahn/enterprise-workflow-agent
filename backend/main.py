import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from anthropic import Anthropic

app = FastAPI()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Schemas ---
class AgentState(BaseModel):
    # What the agent knows to be true (Server-authorized)
    dates_gathered: bool = False
    auth_passed: bool = False
    balance_sufficient: bool = False
    policy_checked: bool = False
    confirmed: bool = False

class TurnRequest(BaseModel):
    message: str
    current_state: AgentState  # Passed by client strictly for Day 1 testing

# --- Stubs ---
def stub_clarify() -> str:
    return "STUB_FIRED: Asked user for missing parameters."

def stub_directory_api() -> str:
    return "STUB_FIRED: Looked up employee balance in database."

def stub_create_pto_request() -> str:
    return "STUB_FIRED: PTO Request successfully written to database."

def stub_refusal(reason: str) -> str:
    return f"STUB_FIRED: Refused action. Reason: {reason}"

# --- The Turn ---
@app.post("/turn")
async def process_turn(request: TurnRequest):
    state = request.current_state

    # 1. LLM Step: Intent Classification (The Decision)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        system="You are an enterprise routing classifier. Analyze the message and pick the next logical route.",
        messages=[{"role": "user", "content": request.message}],
        tools=[{
            "name": "route_intent",
            "description": "Determine the next route.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "route": {
                        "type": "string",
                        "enum": ["clarify", "directory_api", "handbook_rag", "create_pto_request", "refusal"]
                    },
                    "reasoning": {"type": "string"}
                },
                "required": ["route", "reasoning"]
            }
        }],
        tool_choice={"type": "tool", "name": "route_intent"}
    )

    # Extract the structured output
    tool_use = next(block for block in response.content if block.type == "tool_use")
    decision_route = tool_use.input["route"]
    reasoning = tool_use.input["reasoning"]

    action_taken = ""

    # 2. Python Step: Gate Enforcement & Stub Execution (The Act)
    if decision_route == "create_pto_request":
        # The Write Gate: Enforced by Python, not the LLM.
        if not all([state.dates_gathered, state.auth_passed, state.balance_sufficient, state.policy_checked, state.confirmed]):
            action_taken = stub_refusal("Gate Rejected: Missing preconditions for a write action.")
            # State remains unchanged; turn consumed by rejection.
        else:
            action_taken = stub_create_pto_request()

    elif decision_route == "directory_api":
        # The Read Auth Gate
        if not state.auth_passed:
            action_taken = stub_refusal("Gate Rejected: Unauthorized read attempt.")
        else:
            action_taken = stub_directory_api()
            state.balance_sufficient = True # Mocking a successful state update

    elif decision_route == "clarify":
        action_taken = stub_clarify()
        state.dates_gathered = True # Mocking a successful state update

    else:
        action_taken = f"STUB_FIRED: {decision_route} (No strict gate implemented for stub yet)"

    # 3. Return the Turn
    return {
        "llm_decision": decision_route,
        "llm_reasoning": reasoning,
        "action_taken": action_taken,
        "updated_state": state.model_dump()
    }
