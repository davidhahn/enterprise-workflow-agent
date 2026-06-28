1. Backend Architecture: FastAPI vs. Next.js App Router
- The Win: Decoupling the stack into a React frontend and a Python backend signals deep Python competence and mirrors how enterprise FDE teams actually build and deploy microservices.
- The Tradeoff Accepted: I am eating the cost of managing two processes, configuring CORS, serializing data across the wire, and maintaining two deploy targets. More importantly, I am forcing the core agent logic into Python, a language I am still growing in, while on a tight timeline.

2. Orchestration: Anthropic Python SDK
- The Win: Aligns directly with my target ecosystem narrative and leverages Claude's top-tier structured output and tool-calling capabilities.
- The Tradeoff Accepted: I am structurally locking the agent's core routing logic to a single vendor's API surface. By choosing the native Anthropic SDK over a unified wrapper like LiteLLM or LangChain, I am actively making it harder to execute cross-model A/B comparisons (a stated stretch goal of this lab). For a project whose entire thesis is evaluation and reliability, giving up easy multi-provider testing is a massive, on-theme cost that I am choosing to accept for the sake of speed and ecosystem alignment on Day 1.

3. Vector Embeddings: Local Open Source (BGE-M3) vs. Managed API
- The Win: Generating embeddings locally proves I can handle the strict data privacy, zero-network-latency, and air-gapped deployment constraints that enterprise customers demand.
- The Tradeoff Accepted: It introduces heavier backend complexity, a bigger Docker footprint, and the risk of yak-shaving dependency hell.
- Execution Rule (Day 1 vs. Target): This is the target architecture. On Day 1, the RAG tool will strictly be a mocked JSON stub that returns a hardcoded string. `sentence-transformers` and the BGE model will not be installed or wired in until Day 3, when the RAG path is actively being built.
