## Architecture Boundaries: The Stateful Execution Loop

The agent does not use a flat classifier. It executes a stateful loop where each turn's legality depends on accumulated state.

**Turn 1: Parameter Gathering**
*   **Decision:** Clarify (Ask for dates).
*   **Why it's allowed:** Intent is known, but execution parameters are missing.
*   **The wrong move:** Calling a tool before the required parameters exist.

**Turn 2: The Read Auth Gate & Balance Lookup**
*   *Auth Gate Check:* Verify session User ID matches target ID. (Note: This establishes the write-authorization boundary for the entire loop).
*   **Decision:** Call Tool -> `Directory_API`.
*   **Why it's allowed:** Dates gathered, Auth passed. Minimum state to query database is met.
*   **The wrong move:** Moving to a write state before confirming the math.

**Turn 3: Policy Validation**
*   **Decision:** Call Tool -> `Handbook_RAG`.
*   **Why it's allowed:** Auth verified, Balance confirmed sufficient. State requires validating dates against policy.
*   **The wrong move:** Asking for user confirmation before checking company-wide blackout policies.

**Turn 4: The Pre-Write Confirmation Gate**
*   *Write Gate Check:* Explicit human YES/NO for the proposed payload. (Note: This is strictly *confirmation*. *Authorization* was established at Turn 2).
*   **Decision:** Propose Action.
*   **Why it's allowed:** Dates, Auth, Balance, and Policy are all accumulated and validated.
*   **The wrong move:** Executing background writes silently.

**Turn 5: Execution**
*   **Decision:** Call Tool -> `Create_PTO_Request`.
*   **Why it's allowed:** Pre-Write Gate explicitly unlocked by user confirmation.
*   **The wrong move:** Re-running earlier checks or looping backwards.

---

### Cross-Cutting Boundary Rules

**Global Tool Failure Handling**
*   *Rule:* Any tool invocation (`Directory_API`, `Handbook_RAG`, `Create_PTO_Request`) may return a hard failure (e.g., 504 Timeout, 404 Not Found, 403 Forbidden).
*   *Execution:* On hard failure, the agent must immediately halt the sequence, escalate to the user by surfacing the exact degradation, and offer a fallback action (e.g., opening an IT support ticket).
*   *The wrong move:* Catching the error to silently proceed with hallucinated fallback data, assuming a default "safe" state, or entering an infinite, invisible retry loop.
