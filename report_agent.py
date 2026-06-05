from __future__ import annotations
import pandas as pd
from llm_client import LLMRouter


def format_checks(checks: list[str] | None) -> str:

    if not checks:
        return "- No issues detected"

    clean = [str(c) for c in checks if c]

    if not clean:
        return "- No issues detected"

    return "\n".join(f"- {c}" for c in clean)


class ReportAgent:

    def __init__(self):
        self.llm = LLMRouter()

    def generate(
        self,
        metrics_df: pd.DataFrame,
        data_checks: list[str],
        metric_checks: list[str],
    ) -> str:

        metrics_text = metrics_df.to_markdown(index=False)

        prompt = f"""
You are a senior fintech data analyst.

CRITICAL RULES:
- Do NOT stop early
- You MUST complete ALL 7 sections
- Each section MUST have 5–7 bullet points
- NO empty sections allowed
- Return ONLY markdown

STRUCTURE:

# Business Report

## 1. Executive Summary
- 5–7 bullets explaining overall performance

## 2. Monthly Revenue Trend
- 5–7 bullets with quantitative analysis

## 3. Churn Trend
- 5–7 bullets explaining churn dynamics

## 4. ARPU Trend
- 5–7 bullets on monetization

## 5. Data Quality Checks
{format_checks(data_checks)}

## 6. Metric Validation Results
{format_checks(metric_checks)}

## 7. Business Interpretation
- 5–7 bullets: risks, opportunities, recommendations

METRICS:
{metrics_text}

IMPORTANT:
Return full completed markdown report.
"""

        return self.llm.generate(prompt)