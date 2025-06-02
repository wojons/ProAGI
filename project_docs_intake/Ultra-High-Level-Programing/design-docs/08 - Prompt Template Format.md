## 8. Prompt Template Format

LLM Prompts are a fundamental part of defining application logic within the UHLP framework, especially for components using the `LLM` handler type or workflows invoking LLMs [1]. This section specifies the standard format for storing and defining these prompts within the application's state directory, enabling dynamic data injection, metadata management, and structured output expectations [1].

### 8.1. LLM Prompt Template Format Specification (Version 1.0)

#### 8.1.1. Purpose & File Format (YAML)

*   **Purpose:** To provide a standardized, version-controlled format for defining LLM prompts used by UHLP applications. This format facilitates dynamic generation of prompts based on runtime context, allows association of important metadata, and enables specification of desired output structures for improved reliability [1, 2].
*   **File Format:** Prompt templates are defined using **YAML** files [1].
*   **Location:** These YAML files reside within the application's versioned definition state (managed by Git and the `StateManagerInterface`), typically organized in a dedicated subdirectory like `prompts/` (e.g., `prompts/summarize_customer_interaction.yaml`) [1].

#### 8.1.2. Structure (Metadata + `template`)

Each prompt template YAML file follows a structured format, incorporating both the core prompt text and associated metadata [2]:

```yaml
# --- Example: prompts/summarize_customer_interaction.yaml ---

# Optional: Human-readable string describing the prompt's objective.
description: Summarizes a customer interaction transcript, extracting key points and sentiment.

# Optional: Allows overriding the application's default LLM model specifically for this prompt.
# If omitted, the model configured globally for the application (via ApplicationRegistry) is used.
# Example values: "gpt-4-turbo", "claude-3-sonnet", "gemini-1.5-pro"
model: "claude-3-haiku"

# Optional: Default parameters to use for the LLM API call when using this template.
# These parameters can be further overridden by values provided dynamically in the workflow step
# that invokes this prompt. Common LLM parameters include temperature, max_tokens, top_p, etc.
parameters:
  temperature: 0.6
  max_tokens: 500

# Required: The core prompt template string itself. This field contains the text that will be
# processed by the templating engine and sent to the LLM.
template: |
  # --- (Content of the template field below) ---
  Role: You are an AI assistant specialized in analyzing customer support interactions.
  Task: Analyze the following interaction transcript and provide a summary according to the specified JSON format.

  Transcript:
  {{ interaction_transcript }}
  {% if customer_history %}
Additional Customer History Context:
- Loyalty Status: {{ customer_history.loyalty_status | default('N/A') }}
- Recent Issues: {{ customer_history.recent_issues_count | default(0) }}
{% endif %}

Instructions:
1. Read the transcript carefully.
2. Identify the main reason for the customer contact.
3. Determine the overall sentiment of the customer (positive, neutral, negative).
4. Extract any specific action items or follow-ups mentioned.
5. Generate a concise summary (2-3 sentences).

Output Format: Respond ONLY with a valid JSON object containing the keys "main_reason", "sentiment", "action_items", and "summary".

# Optional: A hint indicating the expected format of the LLM's completion text.
# Common values: "json", "text", "xml", "yaml". This helps the framework or orchestrator
# anticipate how to parse or validate the LLM's response. [2]
outputFormat: json

# Optional: A formal JSON Schema definition describing the expected structure and data types
# of the LLM's output, particularly used when outputFormat is "json". [2]
# This schema enables automatic validation of the LLM's response by the framework/orchestrator
# before it's used in subsequent workflow steps, increasing reliability.
outputSchema:
type: object
properties:
  main_reason":
    type: string
    description: "The primary reason the customer initiated contact."
  sentiment:
    type: string
    enum: ["positive", "neutral", "negative"]
    description: "The overall sentiment expressed by the customer."
  action_items":
    type: array
    items:
      type: string
    description: "A list of specific action items or follow-ups required."
  summary:
    type: string
    description: "A concise 2-3 sentence summary of the interaction."
required:
  - main_reason
  - sentiment
  - action_items
  - summary

# Optional (Future V2+): A list of few-shot examples to improve LLM performance for complex tasks.
# Structure TBD, could be a list of objects, each containing example 'input_vars' and the corresponding 'expected_output'.
# examples:
#   - input_vars: { interaction_transcript: "...", customer_history: {...} }
#     expected_output: '{ "main_reason": "Billing query", "sentiment": "neutral", ... }'
```
#### 8.1.3. Templating Engine (Jinja2)

The `template` field within the YAML file is processed using the **Jinja2 templating engine** before being sent to the LLM [2]. This provides powerful capabilities beyond simple variable substitution:

- **Variable Injection:** Dynamically insert data into the prompt using `{{ variableName }}` syntax [2]. Variables are sourced from the `inputMapping` defined in the workflow step or component that invokes this prompt template [1]. Nested data access (e.g., `{{ user.profile.email }}`) is supported.
- **Conditionals:** Include logic within the prompt using `{% if condition %} ... {% elif condition %} ... {% else %} ... {% endif %}` blocks [2]. Conditions can reference context variables.
- **Loops:** Iterate over lists or sequences using `{% for item in item_list %} ... {% endfor %}` blocks, useful for formatting lists of data or examples within the prompt [2].
- **Filters:** Apply transformations to variables using standard Jinja2 filters (e.g., `{{ data | tojson }}`, `{{ text | upper }}`, `{{ value | default('N/A') }}`) and potentially custom filters defined by the framework [2].
- **Markdown Compatibility:** The content within the `template` string can utilize Markdown formatting (headers, lists, code blocks, etc.). This Markdown is rendered as part of the final prompt string sent to the LLM, which can often interpret it effectively for structuring instructions or data presentation.

#### 8.1.4. Output Specification (`outputFormat`, `outputSchema`)

To improve the reliability and predictability of LLM interactions, the template format allows specifying expectations about the LLM's output:

- **`outputFormat`:** A simple string hint (e.g., `"json"`, `"text"`) indicating the expected general format of the LLM's completion [2]. This can guide subsequent parsing steps.
- **`outputSchema`:** For structured outputs (especially JSON), this field allows defining a formal **JSON Schema** [2]. When present, the UHLP framework component (e.g., the workflow orchestrator or MCP wrapper) receiving the LLM's response SHOULD attempt to parse the completion according to the `outputFormat` and then validate the resulting data structure against this schema [2]. Validation failures can be treated as errors, preventing malformed data from propagating through the system and potentially triggering error handling or retry logic.

#### 8.1.5. Processing Flow Summary

1. A workflow step (`type: llm`) or direct component invocation identifies a `promptTemplate` file path [1].
2. The orchestrator/runner loads the YAML file (via `core.state.getDefinitionFileContent`) [1].
3. It prepares the Jinja2 context dictionary based on the `inputMapping` [1].
4. It renders the `template` string using Jinja2 [2].
5. It constructs the final payload for the `core.llm.generate` MCP tool, including the rendered prompt, effective model, and merged parameters [1].
6. It invokes the MCP tool [1].
7. Upon receiving the LLM completion, it optionally parses and validates the output against `outputFormat` and `outputSchema` [2].
8. The (potentially validated) result becomes the output of the LLM step/component [1].