## Brief overview
This Cline rule file provides guidelines for Cline when operating in "YOLO mode" to develop a Proof of Concept (POC) for a software project. The primary goal is to enable Cline to build the POC autonomously, relying heavily on provided documentation and industry best practices, while minimizing direct user input for non-critical steps. This rule is intended to be general enough for reuse but will use the Nexus CoCreate AI POC as an illustrative example where context is beneficial.

## Core Development Principles (YOLO Mode for POC Development)
-   **Documentation as Primary Source of Truth:**
    -   Cline MUST prioritize the main project specification document (e.g., for the current task, the `Nexus_CoCreate_AI-Comprehensive_MVP_POC_Design_Specification.md`) as the primary source for requirements and design.
    -   Supplementary documentation (e.g., in `docs/`, `project_docs_intake/`, `memory-bank/web-research.md` for the Nexus POC) SHOULD be consulted for additional context, research findings, and architectural insights.
-   **Proactive & Iterative Implementation:**
    -   Cline MUST actively build components and features as outlined in the primary specification.
    -   Development SHOULD proceed in logical phases or components, allowing for iterative progress.
-   **Assumption Logging & Best Guess Decisions:**
    -   When ambiguities arise in the specification or minor details are not covered, and direct user input is to be minimized, Cline MUST make informed, best-guess decisions based on:
        1.  The overall project vision and goals.
        2.  Industry best practices and common software engineering patterns.
        3.  Information gleaned from related project documentation (e.g., `memory-bank/web-research.md` for technology choices).
    -   All significant assumptions and best-guess decisions MUST be clearly logged (e.g., in `activeContext.md` or a dedicated task log) for later review by the user.
-   **Focus on MVP/POC Scope:**
    -   Cline MUST strictly adhere to the defined scope for the Minimum Viable Product (MVP) or Proof of Concept, avoiding feature creep unless a deviation is logged as a critical necessity.

## Technology & Tooling Guidelines
-   **Open Source First:**
    -   When selecting libraries, frameworks, or tools, Cline SHOULD strongly prefer mature, well-maintained open-source options, as guided by project documentation (e.g., the "Open Source Leverage" section in the Nexus MVP spec).
-   **Language & Framework Adherence:**
    -   Cline MUST use the programming languages and frameworks specified in the project documentation (e.g., Python for the Nexus CoCreate AI backend).
-   **Dockerization by Design:**
    -   All components SHOULD be designed with Docker containerization in mind from the outset, facilitating consistent environments and deployment.
-   **Version Control with Git:**
    -   All generated code, configuration files, AppDefinitions, prompts, and other project artifacts MUST be version-controlled using Git in their respective local repositories.
    -   Cline SHOULD make frequent, logical commits with clear messages.

## User Interaction & Reporting
-   **Minimized Clarification for Non-Critical Steps:**
    -   Cline MUST avoid asking clarifying questions for minor implementation details or non-critical steps where a reasonable assumption can be made and logged.
-   **Logging Major Assumptions/Deviations:**
    -   If a significant deviation from the primary specification seems necessary due to unforeseen technical challenges, or if a major ambiguity arises that could fundamentally block progress or lead to substantial rework, Cline MUST:
        1.  Document the issue clearly.
        2.  Outline the rationale for the chosen best-guess solution or deviation.
        3.  Log the assumption made.
        4.  Proceed with the best-guess solution. This log serves as a record for later user review.
-   **Regular Progress Updates:**
    -   Cline SHOULD provide periodic updates on completed components, current work, and next steps, allowing the user to passively monitor progress.
-   **Error Reporting:**
    -   If critical errors or insurmountable blockers are encountered that prevent further progress even with best-guess assumptions, Cline MUST report these clearly to the user.

## Adherence to Project-Specific Requirements
-   While this rule provides general guidelines for YOLO POC development, Cline MUST always prioritize and meticulously follow the detailed requirements laid out in the primary specification document for the specific POC being developed (e.g., `Nexus_CoCreate_AI-Comprehensive_MVP_POC_Design_Specification.md`). This includes UI/UX principles, feature sets, architectural decisions, and out-of-scope items defined therein.
