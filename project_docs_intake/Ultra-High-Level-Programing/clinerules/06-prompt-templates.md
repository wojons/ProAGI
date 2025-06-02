# LLM Prompt Template Standards (`06-prompt-templates.md`)

This document outlines standards and best practices for writing LLM Prompt Template YAML files within UHLP applications. These templates are crucial for ensuring consistent, effective, and controllable interactions with Large Language Models (LLMs).

## 1. File Structure & Specification Adherence

*   **File Location:** Store prompt templates within the application's state directory, typically under `prompts/` [1]. Use descriptive filenames (e.g., `summarize_article.yaml`, `generate_user_profile.yaml`).
*   **YAML Format:** Strictly adhere to the **`LLM Prompt Template Format Specification (Version 1.0)`** [1]. Ensure all required and relevant optional fields are used correctly.
*   **Metadata:**
    *   **`description`:** Always include a clear `description` explaining the prompt's purpose and intended use case [2].
    *   **`model` (Optional):** Specify only if this prompt requires a *different* model than the application's default [2]. Avoid unnecessary overrides.
    *   **`parameters` (Optional):** Define default LLM parameters (like `temperature`, `max_tokens`) only if specific settings are generally recommended for this prompt [2]. Allow workflow steps to override these defaults flexibly.

## 2. Jinja2 Template (`template:`) Best Practices [2]

*   **Clarity:** Write Jinja2 logic that is easy to understand. Use comments `{# Jinja comment #}` for complex template logic.
*   **Variable Usage:** Use descriptive variable names (`{{ descriptive_name }}`) consistent with the input data mapped in workflow steps [1].
*   **Data Preparation:** Prefer preparing complex data structures or performing heavy logic in preceding `jit` or `control` workflow steps rather than embedding overly complex Jinja2 logic within the prompt template itself. The template should focus on *presenting* the data to the LLM effectively.
*   **Conditionals & Loops:** Use `{% if %}` and `{% for %}` sparingly for including/excluding sections or formatting lists based on input data. Avoid deeply nested logic if possible [2].
*   **Filters:** Utilize standard Jinja2 filters (e.g., `| tojson`, `| default('N/A')`, `| length`) appropriately for formatting or handling missing data.

## 3. Prompt Text Content Best Practices

*   **Clear Instructions:** State the LLM's task, role (e.g., "You are a helpful assistant...", "Act as an expert data analyst..."), and desired output format explicitly and unambiguously at the beginning or end of the prompt.
*   **Context is Key:** Provide sufficient context for the LLM to perform the task. Use the Jinja2 template to inject relevant data (`userData`, `previousStepsOutput`, etc.) clearly formatted (e.g., using Markdown code blocks for JSON/data snippets).
*   **Structure & Formatting:** Use Markdown (headings, lists, code blocks) within the prompt text to structure information clearly for the LLM.
*   **Specificity:** Be specific about constraints, desired tone, length limits, and information sources (e.g., "Based *only* on the provided text...", "Respond in a friendly, professional tone.").
*   **Input/Output Examples (Few-Shot):** When feasible and beneficial (especially for complex formatting or reasoning tasks), consider adding few-shot examples. *(Note: The YAML structure for `examples` is TBD/V2, but anticipate its potential use)*.
*   **Iterative Refinement:** Prompt engineering is iterative. Expect to test and refine prompt text based on LLM outputs during development.

## 4. Output Specification (`outputFormat`, `outputSchema`) [2]

*   **`outputFormat`:** Always specify the intended `outputFormat` (e.g., `json`, `text`, `yaml`) to guide the LLM and downstream parsing logic [2].
*   **`outputSchema` (for JSON):** If `outputFormat` is `json`, **strongly recommend** providing a precise `outputSchema` using JSON Schema syntax [2].
    *   This enables automatic validation of the LLM's output by the framework/runner.
    *   Define required fields, data types, enums, and nested structures accurately.
    *   This significantly improves the reliability of using LLM outputs in subsequent workflow steps.

## 5. Security Considerations

*   **No Secrets in Templates:** **DO NOT** embed sensitive information (API keys, credentials, PII hints beyond necessary context) directly within prompt template text or examples. Inject required sensitive inputs carefully via the secure context passed during workflow execution.
*   **Prompt Injection Risk:** Be aware of the potential for prompt injection if user-provided data is inserted directly into the template without sanitization or clear demarcation. Structure prompts to clearly separate instructions from potentially untrusted input data (e.g., using code blocks or specific delimiters).

## 6. Maintainability

*   **Comments:** Add YAML comments (`#`) to explain metadata choices, complex Jinja2 logic, or specific prompt instructions.
*   **Modularity:** Create separate template files for distinct LLM tasks rather than monolithic templates trying to do too much.
*   **Versioning:** Use workflow/application versioning to manage changes to prompts over time.
