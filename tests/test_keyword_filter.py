from zotero_arxiv_daily.keyword_filter import keyword_match_score, filter_papers_by_keywords
from zotero_arxiv_daily.protocol import Paper


def test_keyword_match_score_exact_phrase():
    text = "A World Model for Video Generation"
    assert keyword_match_score(text, "World Model") == 1.0


def test_keyword_match_score_token_overlap():
    text = "Physics constrained neural networks"
    # only one token in "Physics-informed" can be matched
    assert keyword_match_score(text, "Physics-informed") == 0.5


def test_filter_papers_by_keywords_any_keyword_match():
    papers = [
        Paper(source="arxiv", title="World Model for Control", authors=[], abstract="", url="u1"),
        Paper(source="arxiv", title="Diffusion for Images", authors=[], abstract="", url="u2"),
        Paper(source="arxiv", title="Data-driven methods", authors=[], abstract="Physics constrained system", url="u3"),
    ]
    keywords = {"World Model": 0.5, "Physics-informed": 0.8}
    filtered = filter_papers_by_keywords(papers, keywords)
    assert [p.url for p in filtered] == ["u1"]