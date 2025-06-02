# UHLP Documentation Standards (`10-documentation.md`)

This document outlines the documentation requirements and standards for the UHLP framework project. Clear, comprehensive, and up-to-date documentation is crucial for developers working on the framework, users building UHLP applications, and long-term maintainability.

## 1. Code Documentation (Docstrings)

*   **Target Language (Python Example):**
    *   **Requirement:** All public modules, classes, functions, and methods **MUST** have clear docstrings following PEP 257 [1].
    *   **Style:** Use Google style or NumPy style docstrings consistently.
    *   **Content:** Docstrings must clearly explain:
        *   The purpose of the object/function/method.
        *   Arguments (`Args:` section): Name, type, and description of each argument.
        *   Return values (`Returns:` section): Type and description of the return value(s).
        *   Exceptions Raised (`Raises:` section): Types of exceptions that can be raised and under what conditions.
        *   Usage examples (`Example:` section) are encouraged for complex functions.
*   **Other Languages:** Follow idiomatic documentation standards for the respective language (e.g., JSDoc for TypeScript/JavaScript, Go Doc comments).

## 2. Inline Code Comments

*   **Purpose:** Use inline comments (`#` in Python/YAML, `//` in JS/Go) sparingly to explain *why* a particular piece of code exists, not *what* it does (the code itself should be clear).
*   **Use Cases:** Explain complex algorithms, non-obvious logic, workarounds for specific issues, or the intent behind certain design choices.
*   **TODO/FIXME:** Use standard markers like `# TODO:` or `# FIXME:` with a brief explanation and ideally a reference (like a ticket number or author initials) for items needing future attention. Keep these temporary.

## 3. Project Documentation (Repository Level)

*   **`README.md`:** [1]
    *   **Requirement:** The root `README.md` **MUST** provide a concise overview of the UHLP project.
    *   **Content:** Should include: project goal, core concepts summary, links to detailed design documents (like the main Design Spec), quick start guide for setting up a development environment, basic usage examples, contribution guidelines, and license information.
    *   **Keep Updated:** Must be kept in sync with major architectural decisions and new capabilities [1].
*   **`CHANGELOG.md`:** [1]
    *   **Requirement:** Maintain a `CHANGELOG.md` file following the Keep a Changelog format.
    *   **Content:** Log significant changes (features, bug fixes, breaking changes) for each version/release.
*   **Design Documents:**
    *   **Primary Spec:** The comprehensive **UHLP Framework Design Specification** document (the one we are assembling) serves as the primary architectural blueprint. It must be kept accurate and versioned.
    *   **ADRs (Architecture Decision Records):** Create Architecture Decision Records (ADRs) in a designated `/docs/adr` directory for significant architectural choices [1]. Use a standard template (like Markdown Architectural Decision Records). Examples requiring ADRs [1]:
        *   Major dependency changes (e.g., switching web frameworks, changing database engines).
        *   Significant architectural pattern changes (e.g., adopting event sourcing).
        *   Introduction of new core integration patterns.
        *   Major database schema changes for framework-managed data.
*   **`/docs` Directory:** Use a `/docs` directory for storing detailed documentation, including the main Design Spec, ADRs, usage guides, tutorials, and potentially diagrams [1].

## 4. API Documentation

*   **Internal APIs (gRPC):**
    *   The `.proto` files defining gRPC services and messages serve as the primary API contract documentation [1].
    *   Include clear comments within the `.proto` files explaining services, methods, messages, and fields.
    *   Consider generating documentation from `.proto` files using tools like `protoc-gen-doc`.
*   **HTTP APIs (Sandbox `/execute`, MCP):**
    *   **Requirement:** All HTTP APIs (including the Sandbox `/execute` and MCP tools) **MUST** be documented using the **OpenAPI Specification (OAS) v3.x** [2].
    *   **Format:** Write OpenAPI specifications in YAML format (`openapi.yaml`).
    *   **Content:** Specs must accurately define paths, operations, parameters (path, query, header, cookie), request bodies (with schemas), responses (with schemas for different status codes), and security schemes. Use JSON Schema for defining data structures within request/response bodies.
    *   **Location:** Store OpenAPI specs logically (e.g., within `/docs/api` or alongside the component implementing the API).
    *   **Automation:** Consider using tools/frameworks that can generate OpenAPI specs from code annotations (e.g., FastAPI) where applicable, but ensure the generated spec is complete and accurate.

## 5. Workflow & Prompt Documentation

*   **Workflow YAML:** Use the `description` field within the Workflow YAML file extensively to explain the overall workflow purpose [1]. Add comments (`#`) within the YAML to clarify specific steps or complex logic [1].
*   **Prompt Templates:** Use the `description` field within the Prompt Template YAML file to explain the prompt's goal and usage [2]. Add comments (`#`) for non-obvious Jinja2 logic or specific instructions within the template text [2].

## 6. General Guidelines

*   **Audience:** Consider the intended audience for the documentation (framework developers, application builders, operators). Tailor the level of detail and language appropriately.
*   **Clarity & Conciseness:** Write clearly and avoid jargon where possible. Be concise but thorough.
*   **Accuracy:** Documentation **MUST** be kept accurate and up-to-date as the code and architecture evolve. Outdated documentation is often worse than no documentation. Integrate documentation updates into the development workflow (e.g., part of the Definition of Done for features/changes).
*   **Discoverability:** Organize documentation logically (e.g., within the `/docs` directory). Ensure the main `README.md` provides clear links to key documents.
