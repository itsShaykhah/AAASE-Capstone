"""Turns a finished CampaignResult into Markdown or PDF for download.

This is the only place that knows how to render a campaign for export —
the API and UI both call it rather than building their own formatting, so
the two export formats can never drift apart.

No persistence is involved: exports are generated on demand from the
result already held in the caller's memory (the API response / Streamlit
session state), matching the "no database" constraint for v1.
"""

from __future__ import annotations

from fpdf import FPDF

from app.schemas.campaign_result import CampaignResult


class ExportService:
    def to_markdown(self, result: CampaignResult) -> str:
        request = result.request
        sections: list[str] = [f"# Marketing Campaign: {request.product_name}", ""]
        sections.append(f"*Generated {result.generated_at.isoformat()} — trace `{result.trace_id}`*")
        sections.append("")

        sections.append("## Product Brief")
        sections.append(f"- **Objective:** {request.campaign_objective.value.replace('_', ' ').title()}")
        if request.target_audience:
            sections.append(f"- **Requested audience:** {request.target_audience}")
        if request.campaign_duration_days:
            sections.append(f"- **Duration:** {request.campaign_duration_days} days")
        sections.append(f"- **Description:** {request.product_description}")
        sections.append("")

        if result.market_intelligence:
            mi = result.market_intelligence
            sections.append("## Market Research Report")
            sections.append(f"**Target audience:** {mi.target_audience}")
            sections.append("")
            sections.append("**Competitors:**")
            sections.extend(f"- {c.name} — {c.notes}" for c in mi.competitors)
            sections.append("")
            sections.append("**Market trends:**")
            sections.extend(f"- {t}" for t in mi.market_trends)
            sections.append("")
            sections.append(f"**Summary:** {mi.summary}")
            sections.append("")

        if result.campaign_strategy:
            cs = result.campaign_strategy
            sections.append("## Campaign Strategy")
            sections.append(f"**Goal:** {cs.campaign_goal}")
            sections.append(f"**Channels:** {', '.join(cs.marketing_channels)}")
            sections.append("")
            sections.append("**Content calendar:**")
            sections.extend(f"- Day {e.day} — {e.channel}: {e.theme}" for e in cs.content_calendar)
            sections.append("")
            sections.append("**Budget allocation:**")
            sections.extend(f"- {b.channel}: {b.percentage:.0f}%" for b in cs.budget_allocation)
            sections.append("")
            sections.append(f"**Summary:** {cs.strategy_summary}")
            sections.append("")

        final_content = result.quality_review.final_content if result.quality_review else result.content_package
        if final_content:
            sections.append("## Final Reviewed Campaign")
            sections.append(f"**Brand voice:** {final_content.brand_voice.tone} — {final_content.brand_voice.voice_description}")
            sections.append("")
            sections.append("### Instagram Caption")
            sections.append(final_content.instagram_caption)
            sections.append("")
            sections.append("### X Post")
            sections.append(final_content.x_post)
            sections.append("")
            sections.append("### LinkedIn Post")
            sections.append(final_content.linkedin_post)
            sections.append("")
            sections.append("### Email Campaign")
            sections.append(f"**Subject:** {final_content.email_campaign.subject_line}")
            sections.append("")
            sections.append(final_content.email_campaign.body)
            sections.append("")
            sections.append("### Ad Headlines")
            sections.extend(f"- {h}" for h in final_content.ad_headlines)
            sections.append("")
            sections.append(f"### Hashtags\n{' '.join(final_content.hashtags)}")
            sections.append("")
            sections.append(f"### Call to Action\n{final_content.call_to_action}")
            sections.append("")

        if result.quality_review:
            qr = result.quality_review
            sections.append("## Quality Assurance")
            sections.append(f"**Overall approved:** {'Yes' if qr.overall_approved else 'No'}")
            sections.extend(f"- {c.check_name}: {c.status.value} — {c.notes}" for c in qr.checks)
            sections.append("")
            sections.append(f"**Notes:** {qr.final_notes}")
            sections.append("")

        return "\n".join(sections)

    def to_pdf(self, result: CampaignResult) -> bytes:
        markdown = self.to_markdown(result)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        for raw_line in markdown.split("\n"):
            # Core PDF fonts only support latin-1; LLM output can contain
            # emoji/smart quotes, so degrade those characters instead of
            # crashing the export.
            line = raw_line.encode("latin-1", errors="ignore").decode("latin-1")
            # multi_cell's default cursor behavior leaves x at the *right*
            # margin (new_x="RIGHT") rather than resetting to the left, so
            # every call below pins it back to LMARGIN/NEXT explicitly —
            # otherwise the following call sees zero horizontal space left.
            if line.startswith("# "):
                pdf.set_font("Helvetica", "B", 16)
                pdf.multi_cell(0, 10, line[2:], new_x="LMARGIN", new_y="NEXT")
            elif line.startswith("## "):
                pdf.set_font("Helvetica", "B", 13)
                pdf.multi_cell(0, 9, line[3:], new_x="LMARGIN", new_y="NEXT")
            elif line.startswith("### "):
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 8, line[4:], new_x="LMARGIN", new_y="NEXT")
            elif line.strip() == "":
                pdf.ln(2)
            else:
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, line.replace("**", ""), new_x="LMARGIN", new_y="NEXT")

        return bytes(pdf.output())
