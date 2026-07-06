"""IEEE paper section writer — LLaMA 3.3-70B grounded in FAISS retrieval."""
from __future__ import annotations

import json
from collections.abc import Callable

from shared.config import SMART_MODEL
from shared.llm import chat

SYSTEM = (
    "You are an expert academic writer producing IEEE conference paper sections. "
    "Write formal, precise, third-person technical prose. Plain paragraphs only: "
    "no markdown, no headings, no bullet lists, no code fences."
)

# (section, retrieval query, length guidance)
SECTIONS: list[tuple[str, str, str]] = [
    ("Abstract", "project purpose main features summary", "150-200 words, one paragraph"),
    ("Introduction", "problem motivation background goals readme overview", "300-400 words, 2-3 paragraphs"),
    ("Methodology", "architecture design approach algorithm pipeline modules", "350-450 words"),
    ("Implementation", "code implementation functions classes configuration setup", "350-450 words"),
    ("Results", "features output performance capabilities usage", "250-350 words"),
    ("Conclusion", "summary limitations future work roadmap", "200-300 words"),
    ("References", "technologies libraries frameworks dependencies", "6-9 numbered entries"),
]


def generate_paper(
    vectorstore,
    analysis: dict,
    meta: dict,
    progress: Callable[[str], None] | None = None,
) -> dict[str, str]:
    """Return {section_name: text} for all seven IEEE sections."""
    analysis_json = json.dumps(analysis, indent=2)
    sections: dict[str, str] = {}

    for name, query, length in SECTIONS:
        if progress:
            progress(name)

        docs = vectorstore.similarity_search(query, k=5)
        context = "\n\n---\n\n".join(d.page_content for d in docs)[:6000]

        if name == "References":
            prompt = f"""Write the References section for an IEEE paper about the repository {meta['full_name']}.

Project analysis:
{analysis_json}

List {length} in IEEE citation style ([1], [2], ...). Cite only: the repository itself
({meta['html_url']}), its documentation, and the official documentation or canonical
papers of the technologies actually used ({', '.join(analysis.get('technologies', []))}).
Do not invent authors, journals, or page numbers for sources you are not certain exist."""
        else:
            prompt = f"""Write the {name} section of an IEEE conference paper about this software project.

Project analysis:
{analysis_json}

Relevant repository excerpts:
{context}

Length: {length}. Ground every claim in the analysis and excerpts above.
Return only the section text — do not repeat the section title."""

        sections[name] = chat(prompt, system=SYSTEM, model=SMART_MODEL, temperature=0.4)

    return sections
