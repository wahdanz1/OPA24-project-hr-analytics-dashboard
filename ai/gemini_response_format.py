def get_response_format() -> str:
    """
    Plain-text instructions sent to Gemini that describe EXACTLY how it must
    structure every reply.  Paste this verbatim into your prompt assembly.
    """
    return """
╔══════════════════════════════════════════════════════════════════╗
║                        JSON-ONLY FORMAT                          ║
╚══════════════════════════════════════════════════════════════════╝

🔴  Output **one single JSON object**.  
    • NO Markdown fences such as ```json …``` or ``` …```.  
    • NO extra commentary outside the braces.  
    • Keys must appear exactly as spelled below.

Schema
------
- "response"        : <string>            # Text shown to the human user.
- "methods"         : <list>|null         # Each item: {"name": <str>, "args": <dict>}
- "query"           : <string>|null       # SQL-like query for the database.
- "prompt_to_self"  : <string>|null       # REQUIRED when "stop" is false.
- "stop"            : <boolean>           # true → wait for user, false → keep working.

Hard Rules
----------
1. If you need more input from the **human user** → set `"stop": true` and  
   OMIT "query", "methods", and "prompt_to_self".
2. If you will continue autonomously → set `"stop": false` **and** include  
   at least one of "query" or "methods" plus a non-empty "prompt_to_self".
3. Never wrap the JSON in Markdown. Never add extra keys.

Golden Template
---------------
{
  "response": "…",
  "query": null,
  "methods": null,
  "prompt_to_self": null,
  "stop": true
}

Examples
--------

✅ **GOOD – asks user, stop true**
{
  "response": "Which occupation would you like to analyse?",
  "query": null,
  "methods": null,
  "prompt_to_self": null,
  "stop": true
}

✅ **GOOD – autonomous step, stop false**
{
  "response": "Retrieving top employers…",
  "query": "SELECT employer_name, COUNT(*) AS job_count FROM …",
  "methods": null,
  "prompt_to_self": "Now that I have counts, create a bar chart.",
  "stop": false
}

❌ **BAD – Markdown fence (NOT allowed)**
```json
{ "response": "…" }"""