"""
ai_service.py

Generates AI recommendations and executive summaries for failed
validation results, using Groq. Falls back to a templated
explanation (no LLM call) if GROQ_API_KEY is not set, so the app
runs end-to-end even before you wire up a key.

Author: Raman Tiwari
Project: SAP AI Test Agent
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

_GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

_client = None
if _GROQ_API_KEY:
    from groq import Groq
    _client = Groq(api_key=_GROQ_API_KEY)


def _fallback_recommendation(failed_result: dict) -> str:
    count = failed_result.get("count", 1)
    scope = (
        f"This affects {count} record(s), for example {failed_result['entity']}."
        if count > 1 else
        f"This affects {failed_result['entity']}."
    )
    return (
        f"[{failed_result['severity']}] {failed_result['rule_name']}: "
        f"{failed_result['message']} {scope} "
        f"Review and correct before the process continues."
    )


def generate_recommendation(failed_result: dict) -> str:
    """
    Generate a one-paragraph AI recommendation for a failed check.
    failed_result may represent a single instance or, when 'count' is
    present and > 1, a whole cluster of failures sharing the same root
    cause (e.g. all POs blocked by one unapproved vendor) - the prompt
    is written to summarize the pattern, not just the one example.
    """

    if _client is None:
        return _fallback_recommendation(failed_result)

    count = failed_result.get("count", 1)
    scope_line = (
        f"This pattern affects {count} records. Example: {failed_result['entity']}.\n"
        if count > 1 else
        f"Entity: {failed_result['entity']}\n"
    )

    prompt = (
        "You are a senior SAP MM functional consultant reviewing a failed "
        "automated test. Explain briefly why this matters and the concrete "
        "fix, in 2-3 sentences, plain text, no markdown. If this affects "
        "multiple records, address it as one pattern, not one record.\n\n"
        f"Rule: {failed_result['rule_name']}\n"
        f"{scope_line}"
        f"Severity: {failed_result['severity']}\n"
        f"Details: {failed_result['message']}\n"
    )

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _fallback_recommendation(failed_result)


def generate_executive_summary(results: list[dict]) -> str:
    """
    Generate a short executive summary across all validation results.
    """

    total = len(results)
    failed = [r for r in results if not r["passed"]]

    if _client is None:
        if not failed:
            return f"All {total} checks passed. No issues detected in this run."
        critical = sum(1 for r in failed if r["severity"] == "CRITICAL")
        return (
            f"{len(failed)} of {total} checks failed, including {critical} "
            f"critical issue(s). Review the recommendations below before "
            f"proceeding to the next process step."
        )

    prompt = (
        "You are summarizing an automated SAP procurement test run for a "
        "manager. Write 2-3 plain-text sentences, no markdown.\n\n"
        f"Total checks: {total}\n"
        f"Failed checks: {len(failed)}\n"
        "Failures:\n"
        + "\n".join(f"- {r['rule_name']} ({r['severity']}): {r['message']}" for r in failed[:15])
    )

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"{len(failed)} of {total} checks failed. See recommendations below."


# =====================================================
# ABAP Copilot — review / optimize / convert / document
#
# Grounded in general, public ABAP/SAP best practices only (SELECT *,
# nested SELECT/LOOP, missing FOR ALL ENTRIES, secondary indexes,
# naming, dead code, etc.) — NOT your company's actual coding
# standards. Treat findings as a starting point for a functional/
# technical consultant, not a verdict.
# =====================================================

import json
import re

_ABAP_SYSTEM_CONTEXT = (
    "You are a senior SAP ABAP performance and code-quality reviewer. "
    "You know standard, widely-documented ABAP best practices (avoid "
    "SELECT *, avoid nested SELECT/LOOP, use FOR ALL ENTRIES or JOINs, "
    "secondary indexes, modern ABAP 7.5+ syntax, CDS Views, AMDP, clean "
    "code naming). You do NOT know this specific company's internal "
    "coding standards or naming conventions - never claim to."
)


def _extract_json(text: str) -> dict | None:
    """
    Strips markdown code fences if present and parses JSON. Returns
    None (not an exception) on failure, so callers can fall back
    cleanly instead of crashing the request.
    """
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        return None


def _abap_fallback(mode: str) -> dict:
    return {
        "mode": mode,
        "summary": (
            "AI analysis requires GROQ_API_KEY to be set. Add it to your "
            ".env file to enable ABAP review, optimization, conversion, "
            "and documentation."
        ),
        "score": None,
        "issues": [],
        "optimized_code": None,
        "converted_code": None,
        "documentation": None,
    }


def _call_json(prompt: str, system_context: str | None = None, max_tokens: int = 2000) -> dict | None:
    if _client is None:
        return None

    messages = []
    if system_context:
        messages.append({"role": "system", "content": system_context})
    messages.append({"role": "user", "content": prompt})

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            max_tokens=max_tokens,
        )
        return _extract_json(response.choices[0].message.content)
    except Exception:
        return None


def _call_abap_json(prompt: str, max_tokens: int = 2000) -> dict | None:
    return _call_json(prompt, _ABAP_SYSTEM_CONTEXT, max_tokens)


def analyze_abap(code: str, mode: str, target: str | None = None) -> dict:
    """
    Runs one of four ABAP analysis modes and returns a dict matching
    schemas.AbapAnalyzeResponse. Always returns a usable dict, even on
    parse failure or missing API key - never raises.
    """

    if mode == "review":
        prompt = (
            "Review this ABAP code for performance, readability, security, "
            "and complexity. Respond with ONLY valid JSON, no markdown, no "
            "prose outside the JSON, matching exactly this shape:\n"
            '{"summary": "2-3 sentence overview", '
            '"score": {"performance": 0-100, "readability": 0-100, '
            '"security": 0-100, "complexity": 0-100}, '
            '"issues": [{"severity": "CRITICAL|HIGH|MEDIUM|LOW", '
            '"title": "short title", "description": "1-2 sentences"}]}\n\n'
            f"ABAP code:\n```\n{code}\n```"
        )
        result = _call_abap_json(prompt) or _abap_fallback(mode)

    elif mode == "optimize":
        prompt = (
            "Find performance and quality issues in this ABAP code (SELECT *, "
            "nested SELECT/LOOP, missing FOR ALL ENTRIES, missing secondary "
            "indexes, dead code, bad naming) and produce an optimized version. "
            "Respond with ONLY valid JSON, no markdown, no prose outside the "
            "JSON, matching exactly this shape:\n"
            '{"summary": "2-3 sentence overview of what changed and why", '
            '"issues": [{"severity": "CRITICAL|HIGH|MEDIUM|LOW", '
            '"title": "short title", "description": "1-2 sentences"}], '
            '"optimized_code": "the full optimized ABAP code as a string, '
            'with \\n for newlines"}\n\n'
            f"ABAP code:\n```\n{code}\n```"
        )
        result = _call_abap_json(prompt, max_tokens=3000) or _abap_fallback(mode)

    elif mode == "convert":
        target_label = {
            "abap_740": "ABAP 7.40 syntax (inline declarations with DATA(), "
                        "VALUE and COND constructors)",
            "abap_750": "ABAP 7.50 syntax (table expressions itab[ ...], the "
                        "NEW operator, FOR expressions)",
            "abap_752": "ABAP 7.52 syntax (REDUCE, CORRESPONDING with mapping, "
                        "further table expression capabilities)",
            "abap_cloud": "ABAP for Cloud / RAP-ready syntax (restricted to "
                          "cloud-compatible statements only, no obsolete or "
                          "released-for-cloud-incompatible constructs)",
            "abap_oo": "ABAP Objects (an object-oriented refactor of this "
                       "procedural logic into classes and methods)",
            "rap": "a RAP (RESTful ABAP Programming Model) behavior "
                   "definition and business object outline",
            "cds_view": "an SAP CDS View definition",
            "amdp": "an AMDP (ABAP Managed Database Procedure) method",
            "python": "equivalent Python code (this is a translation of "
                      "logic/intent, not a runnable SAP integration)",
            "cap": "a CAP (Cloud Application Programming Model) service "
                   "definition, Node.js/CDS style (conceptual translation, "
                   "not a runnable SAP integration)",
        }.get(target or "abap_750", "modern ABAP 7.50 syntax")

        prompt = (
            f"Convert this ABAP code to {target_label}. Respond with ONLY "
            "valid JSON, no markdown, no prose outside the JSON, matching "
            "exactly this shape:\n"
            '{"summary": "2-3 sentence overview of the conversion", '
            '"explanation": "why this form is better/different, 2-4 '
            'sentences", '
            '"converted_code": "the full converted code as a string, with '
            '\\n for newlines"}\n\n'
            f"ABAP code:\n```\n{code}\n```"
        )
        raw = _call_abap_json(prompt, max_tokens=3000)
        if raw:
            result = {
                "mode": mode,
                "summary": raw.get("summary", ""),
                "converted_code": raw.get("converted_code"),
                "documentation": None,
                "issues": [],
                "score": None,
                # stash explanation inside summary since schema has no
                # separate field for it - keeps the API shape stable
                "explanation": raw.get("explanation"),
            }
        else:
            result = _abap_fallback(mode)

    elif mode == "document":
        prompt = (
            "Document this ABAP program for a new team member. Respond with "
            "ONLY valid JSON, no markdown, no prose outside the JSON, "
            "matching exactly this shape:\n"
            '{"summary": "2-3 sentence program purpose", '
            '"documentation": {'
            '"inputs": ["input 1", "..."], '
            '"outputs": ["output 1", "..."], '
            '"tables_used": ["TABLE1", "..."], '
            '"function_modules": ["FM_NAME", "..."], '
            '"business_logic": "paragraph describing what the program does", '
            '"flow": [{"step": "Read MARA"}, {"step": "Loop over items"}, '
            '{"step": "..."}]}}\n\n'
            f"ABAP code:\n```\n{code}\n```"
        )
        result = _call_abap_json(prompt) or _abap_fallback(mode)

    else:
        return {
            "mode": mode,
            "summary": f"Unknown mode '{mode}'.",
            "score": None,
            "issues": [],
            "optimized_code": None,
            "converted_code": None,
            "documentation": None,
        }

    result["mode"] = mode
    result.setdefault("summary", "")
    result.setdefault("issues", [])
    result.setdefault("score", None)
    result.setdefault("optimized_code", None)
    result.setdefault("converted_code", None)
    result.setdefault("documentation", None)

    # Fold the convert-mode explanation into summary for a single
    # readable field, since the schema doesn't carry it separately.
    if mode == "convert" and result.get("explanation"):
        result["summary"] = f"{result['summary']}\n\n{result['explanation']}".strip()

    return result


# =====================================================
# AI Rule & Test Case Generator
#
# Turns a plain-English description into a structured business rule:
# name, severity, a representative SQL query, a Python check, and a
# spread of positive/negative/boundary test cases. Same caveat as
# ABAP Copilot: this is a well-reasoned starting point from general
# SAP MM/SD/FI knowledge, not a verified rule - it hasn't seen your
# company's actual field usage or business process nuances.
# =====================================================

_RULE_SYSTEM_CONTEXT = (
    "You are a senior SAP MM/SD/FI functional consultant and QA architect "
    "designing business validation rules for a Python-based testing agent "
    "that checks Purchase Requisitions, Purchase Orders, Goods Receipts, "
    "Invoices, and Inventory data in a relational (Postgres) database. "
    "Rules must be concrete, specific, and checkable against real "
    "relational data - never vague or hand-wavy."
)


def _rule_fallback() -> dict:
    return {
        "rule_name": "GENERATED_RULE",
        "severity": "MEDIUM",
        "description": (
            "AI generation requires GROQ_API_KEY to be set. Add it to your "
            ".env file to enable rule generation."
        ),
        "sql_query": "-- set GROQ_API_KEY to generate SQL",
        "python_check": "# set GROQ_API_KEY to generate a Python check",
        "expected_result": "",
        "business_impact": "",
        "recommendation": "",
        "test_cases": [],
    }


def generate_rule(description: str, module: str) -> dict:
    """
    Generates a structured business rule (name, severity, SQL,
    Python check, and test cases) from a plain-English description.
    Always returns a usable dict matching schemas.RuleGenerateResponse.
    """

    prompt = (
        f"A user wants a new SAP {module} business validation rule, "
        f'described in their own words as:\n"{description}"\n\n'
        "Design this as a concrete, checkable rule. Respond with ONLY "
        "valid JSON, no markdown, no prose outside the JSON, matching "
        "exactly this shape:\n"
        '{"rule_name": "SHORT_UPPER_SNAKE_CASE_NAME", '
        '"severity": "CRITICAL|HIGH|MEDIUM|LOW", '
        '"description": "1-2 sentence plain description of the rule", '
        '"sql_query": "a representative SQL query (Postgres syntax) that '
        "would surface violating records, with \\n for newlines\", "
        '"python_check": "a short Python function implementing the same '
        "check against SQLAlchemy-style objects, with \\n for newlines\", "
        '"expected_result": "what a passing record looks like", '
        '"business_impact": "1-2 sentences on why this matters to the '
        'business", '
        '"recommendation": "1-2 sentence template recommendation for when '
        'this rule fails", '
        '"test_cases": [{"scenario": "short scenario name", "type": '
        '"POSITIVE|NEGATIVE|BOUNDARY", "expected_result": "pass or fail '
        'and why"}] (include at least one POSITIVE, one NEGATIVE, and one '
        "BOUNDARY case)}"
    )

    result = _call_json(prompt, _RULE_SYSTEM_CONTEXT, max_tokens=2000) or _rule_fallback()

    result.setdefault("rule_name", "GENERATED_RULE")
    result.setdefault("severity", "MEDIUM")
    result.setdefault("description", "")
    result.setdefault("sql_query", "")
    result.setdefault("python_check", "")
    result.setdefault("expected_result", "")
    result.setdefault("business_impact", "")
    result.setdefault("recommendation", "")
    result.setdefault("test_cases", [])

    return result
