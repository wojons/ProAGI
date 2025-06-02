## Brief overview
This rule provides guidelines for developing Proof of Concept (POC) software projects in "YOLO mode," emphasizing autonomous development based on provided documentation and industry best practices, while minimizing direct user input for non-critical steps. It is intended to be general enough for reuse across different POC tasks but is informed by the context of the Nexus CoCreate AI POC.

## Core Development Principles (YOLO Mode for POC Development)
- Autonomous Implementation: Proceed with building components and features as outlined in the primary specification and other provided documentation without requiring explicit user input for minor details or non-critical steps.
- Documentation as Primary Source of Truth: Prioritize the main project specification document (e.g., `Nexus_CoCreate_AI-Comprehensive_MVP_POC_Design_Specification.md`) and supplementary documentation (e.g., in `docs/`, `project_docs_intake/`, `memory-bank/web-research.md`) for requirements and design.
- Best Guess Decisions: When ambiguities arise or details are not covered, make informed, best-guess decisions based on the overall project vision, industry best practices, and information from related documentation. Log significant assumptions or deviations (e.g., in `activeContext.md` or a task log) for later review.
- Focus on MVP/POC Scope: Strictly adhere to the defined scope for the Minimum Viable Product (MVP) or Proof of Concept.

## Technology & Tooling Guidelines
- Open Source Leverage: Strongly prefer mature, well-maintained open-source libraries and tools as guided by project documentation (e.g., `memory-bank/web-research.md`) and industry standards.
- Dockerization: Design and implement components with Docker containerization in mind, aiming for a deployable solution via Docker.

## User Interaction & Reporting
- Minimized Clarification: Avoid asking clarifying questions for minor implementation details where a reasonable assumption can be made and logged.
- Error Reporting: Report critical errors or insurmountable blockers that prevent further progress even with best-guess assumptions.
