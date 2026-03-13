import re
from collections.abc import Mapping
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from .protocol import Paper

__all__ = [
    "keyword_match_score",
    "filter_papers_by_keywords",
]


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def keyword_match_score(text: str, keyword: str) -> float:
    """Return a score in [0,1] for how well a keyword matches a text."""
    normalized_text = _normalize_text(text)
    normalized_keyword = _normalize_text(keyword)
    if not normalized_text or not normalized_keyword:
        return 0.0

    if normalized_keyword in normalized_text:
        return 1.0

    keyword_tokens = [t for t in re.split(r"[^a-z0-9]+", normalized_keyword) if t]
    if not keyword_tokens:
        return 0.0

    matched_tokens = sum(1 for token in keyword_tokens if token in normalized_text)
    return matched_tokens / len(keyword_tokens)


def filter_papers_by_keywords(papers: list["Paper"], keywords: Mapping[str, float] | None) -> list["Paper"]:
    """Keep papers whose title+abstract matches any keyword above its threshold."""
    if not keywords:
        return papers

    filtered: list["Paper"] = []
    for paper in papers:
        text = f"{paper.title}\n{paper.abstract}"
        for keyword, threshold in keywords.items():
            score = keyword_match_score(text, keyword)
            if score >= threshold:
                filtered.append(paper)
                break

    logger.info(f"Keyword filter kept {len(filtered)}/{len(papers)} papers")
    return filtered