# 13. AI Evaluation Framework
## Dimensions
Citation validity, factual consistency, schema validity, tool success, safety controls, relevance, human approval, latency, token use, and cost where available.
## Dataset
Versioned synthetic evaluation cases with expected evidence, allowed tools, required fields, prohibited claims, and reviewer rubric.
## Execution
Run deterministic tests first; invoke configured provider when explicitly enabled; validate output; store metrics and failures; compare prompt/agent versions; block promotion on required failures.
## Failure categories
Unknown citation, unsupported claim, schema mismatch, unauthorized tool, timeout, prompt injection blocked, sensitive-data violation, reviewer rejection.
## Reporting
Trends, prompt comparison, per-agent metrics, failed cases, correlation IDs, and reproducible configuration.
