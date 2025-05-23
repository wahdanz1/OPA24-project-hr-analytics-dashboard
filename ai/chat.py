# streamlit_app.py
import streamlit as st
import json, re, sys
import pandas as pd
from pathlib import Path
from gemini import GeminiHandler

# ──────────────────────────────────────────────────────────────
# 0.  Plot helpers 
# ──────────────────────────────────────────────────────────────
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dashboard.plots import (
    create_horizontal_bar_chart,
    create_vertical_bar_chart,
    create_line_chart,
)
from dashboard.utils import fetch_data_from_db
tools = {
    "create_horizontal_bar_chart": create_horizontal_bar_chart,
    "create_vertical_bar_chart": create_vertical_bar_chart,
    "create_line_chart": create_line_chart,
}

# ──────────────────────────────────────────────────────────────
# 1.  Query helper
# ──────────────────────────────────────────────────────────────
def run_query(sql: str) -> pd.DataFrame:
    st.info(f"Running query: `{sql}`")
    return fetch_data_from_db(sql)

# ──────────────────────────────────────────────────────────────
# 2.  Page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(layout="wide")
st.header("Chat")

# ──────────────────────────────────────────────────────────────
# 3.  DEBUG sidebar
# ──────────────────────────────────────────────────────────────
if "debug_log" not in st.session_state:
    st.session_state.debug_log = []
debug_expander = st.sidebar.expander("🔍 Debug log", expanded=False)
def debug(msg: str, **kv):
    st.session_state.debug_log.append((msg, kv))
def flush_debug():
    with debug_expander:
        while st.session_state.debug_log:
            m, kv = st.session_state.debug_log.pop(0)
            st.write(m)
            if kv:
                st.json(kv)

# ──────────────────────────────────────────────────────────────
# 4.  JSON fence-strip helper
# ──────────────────────────────────────────────────────────────
FENCE_RE = re.compile(r"^\s*```(?:json)?\s*(\{.*\})\s*```$", re.S)
def parse_json_from_llm(raw: str) -> dict:
    m = FENCE_RE.match(raw.strip())
    if m:
        raw = m.group(1)
    return json.loads(raw)

# ──────────────────────────────────────────────────────────────
# 5.  Gemini handler
# ──────────────────────────────────────────────────────────────
gemini = GeminiHandler()
debug("[INIT] GeminiHandler created")

# ──────────────────────────────────────────────────────────────
# 6.  Session state (messages + agent context)
# ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "response_dict" not in st.session_state:
    st.session_state.response_dict = {"stop": True}
# keep last N assistant JSON blobs for context
if "context_buffer" not in st.session_state:
    st.session_state.context_buffer = []         # list[str]
MAX_CONTEXT = 4                                   # send last 4 steps

def build_full_prompt(follow_up: str) -> str:
    """
    Prepend recent assistant JSON objects so Gemini remembers its chain.
    GeminiHandler already adds system/tool/db prompts internally, so
    we only tack on CONTEXT + follow_up text here.
    """
    recent = "\n".join(st.session_state.context_buffer[-MAX_CONTEXT:])
    if recent:
        return f"### PREVIOUS CONTEXT ###\n{recent}\n\n{follow_up}"
    return follow_up

# ──────────────────────────────────────────────────────────────
# 7.  Core executor  (paste this whole function)
# ──────────────────────────────────────────────────────────────
def execute_response_dict(rdict: dict, *, depth=0, max_depth=14) -> dict:
    debug(f"[ENTER] depth={depth}", rdict=rdict)
    query_result = None

    while True:
        if depth >= max_depth:
            st.error("💥 Max depth reached – aborting autonomous loop.")
            debug("[ABORT] reached max_depth", depth=depth)
            flush_debug()
            return {"stop": True}

        # 1) SQL
        if rdict.get("query"):
            debug("[SQL] run_query", sql=rdict["query"])
            query_result = run_query(rdict["query"])

        # 2) Plot calls
        if rdict.get("methods"):
            debug("[PLOTS] executing", methods=rdict["methods"])
            for call in rdict["methods"]:
                name = call.get("name")
                args = call.get("args", {}) or {}

                # always inject the latest DataFrame
                if query_result is not None:
                    args["data"] = query_result

                # ─── NEW: normalise color_column ──────────────────
                # • Empty string ""  → None
                # • Ensure key exists even if Gemini omitted it
                if args.get("color_column", "") == "":
                    args["color_column"] = None
                args.setdefault("color_column", None)
                # ───────────────────────────────────────────────────

                func = tools.get(name)
                if not func:
                    st.warning(f"⚠️ unknown method '{name}'")
                    debug("[WARN] unknown", name=name)
                    continue

                # skip empty DataFrame
                df = args.get("data")
                if isinstance(df, pd.DataFrame) and df.empty:
                    st.warning("⚠️ Query returned no rows – chart skipped.")
                    debug("[SKIP] empty dataframe")
                    continue

                try:
                    fig = func(**args)
                    st.plotly_chart(fig, use_container_width=True)
                    debug("[OK] plotted", name=name)
                except Exception as e:
                    st.error(f"❌ {name} failed: {e}")
                    debug("[ERR] plotting", error=str(e))

        # 3) Assistant text
        if rdict.get("response"):
            with st.chat_message("assistant"):
                st.markdown(rdict["response"])
            st.session_state.messages.append(
                {"role": "assistant", "content": rdict["response"]}
            )
            debug("[TEXT] assistant shown")

        # 4) Stop?
        if rdict.get("stop", True):
            debug("[STOP] returning to user")
            flush_debug()
            return {"stop": True}

        # 5) Continue with prompt_to_self
        follow_up = rdict.get("prompt_to_self")
        if not follow_up:
            st.error("stop=False but prompt_to_self missing – forcing stop.")
            debug("[FORCE STOP] missing prompt_to_self")
            flush_debug()
            return {"stop": True}

        debug("[CALL] Gemini follow-up", prompt=follow_up, depth=depth)
        raw = gemini.get_response(build_full_prompt(follow_up)).text
        debug("[RAW] follow-up", raw=raw)

        try:
            rdict = parse_json_from_llm(raw)
            debug("[PARSE] json ok")
            # keep context
            st.session_state.context_buffer.append(json.dumps(rdict))
        except json.JSONDecodeError as e:
            st.error("Gemini sent invalid JSON – aborting.")
            debug("[ERR] json decode", error=str(e))
            flush_debug()
            return {"stop": True}

        depth += 1


# ──────────────────────────────────────────────────────────────
# 8.  Render chat history
# ──────────────────────────────────────────────────────────────
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# ──────────────────────────────────────────────────────────────
# 9.  Main control flow
# ──────────────────────────────────────────────────────────────
if st.session_state.response_dict.get("stop", True):
    # USER-DRIVEN
    if prompt := st.chat_input("Type your message here…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        raw = gemini.get_response(prompt).text
        debug("[MAIN] raw initial", raw=raw)
        try:
            response_dict = parse_json_from_llm(raw)
            debug("[MAIN] parsed initial", response_dict=response_dict)
            st.session_state.context_buffer.append(json.dumps(response_dict))  # NEW
        except json.JSONDecodeError:
            debug("[MAIN] JSON invalid, fallback plain text")
            response_dict = {"response": raw, "stop": True}

        st.session_state.response_dict = execute_response_dict(response_dict)
else:
    # AGENT-DRIVEN resume
    debug("[MAIN] resume autonomous", cached=st.session_state.response_dict)
    if not isinstance(st.session_state.response_dict, dict):
        st.error("Cached response_dict corrupted – resetting.")
        debug("[ERR] cached invalid"); st.session_state.response_dict = {"stop": True}; flush_debug()
    else:
        st.session_state.response_dict = execute_response_dict(st.session_state.response_dict)
        if st.session_state.response_dict.get("stop", True):
            debug("[MAIN] autonomous loop finished, user input enabled")
    flush_debug()
