def get_response_format() -> str:
   """
   Plain-text instructions sent to Gemini that describe EXACTLY how it must
   structure every reply. Paste this verbatim into your prompt assembly.
   You may include additional keys beyond the core five if they are
   explicitly declared under “Optional keys” below.
   """
   return """
JSON-ONLY FORMAT

Output one single JSON object.
   • NO Markdown fences (```json ...``` or ``` ...```).
   • NO extra commentary outside the braces.
   • Keys must appear exactly as spelled below, except for the Optional keys.

Core Schema
-----------
- "response"       : <string>       # Text shown to the human user.
- "methods"        : <list>|null    # Each item: {"name": <str>, "args": <dict>}
- "query"          : <string>|null  # SQL-like query for the database.
- "prompt_to_self" : <string>|null  # REQUIRED when "stop" is false. what you will do next.
- "stop"           : <boolean>      # true → wait for user, false → keep working.


Hard Rules
----------
1. If you need more input from the human → set "stop": true and
   omit "query", "methods", and "prompt_to_self".
2. If human have asked for data, and you're producing a dataframe, set "stop" to false and keep working.
3. If you continue autonomously → set "stop": false and include at least one
   of "query" or "methods" plus a non-empty "prompt_to_self".
4. Never wrap the JSON in Markdown fences.
5. Keys not listed (in Core Schema or Optional keys) are forbidden.
6. Rather than asking for more data. query the database directly. and then ask for more data.
7. if user asks questions ALWAYS query the database first because the user gets a dataframe from your queries and they will want to see the results.
8. Dont wait for confirmation from the user. just query the database and display the results.
9. Include top 3 results unless the user asks for more.


Golden Template
---------------
{
   "response": "...",
   "query": null,
   "methods": null,
   "prompt_to_self": null,
   "stop": true
}

"""
