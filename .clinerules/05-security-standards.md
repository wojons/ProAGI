# Security Standards

This document outlines security standards for the ProAGI project, drawing from previous project guidelines.

- NEVER hardcode secrets or API keys. (Ref: 08-security.md)
- Rigorously validate and sanitize inputs, especially for file paths, database queries, command execution. (Ref: 08-security.md)
- When using `core.linux.executeCommand`, prioritize hardened wrappers and avoid shell interpretation. (Ref: 08-security.md)
