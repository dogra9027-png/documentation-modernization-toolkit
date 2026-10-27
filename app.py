
"""Web interface for the documentation knowledge assistant."""

import re
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
DOCS_DIR = ROOT / "docs"

sys.path.insert(0, str(SCRIPTS_DIR))

from search_docs import load_articles, search_articles


st.set_page_config(
    page_title="Documentation Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Documentation Knowledge Assistant")

st.write(
    "Ask a question about the sample knowledge articles. "
    "Answers are based on retrieved documentation, with source references."
)

st.info(
    "Demo limitation: this version retrieves matching documentation "
    "passages. It does not use an LLM to generate answers."
)


@st.cache_data
def get_articles():
    """Load the Markdown knowledge articles."""
    return load_articles(DOCS_DIR)


def clean_article_links(content):
    """Remove broken local web links while preserving their labels."""
    return re.sub(
        r"\[([^\]]+)\]\((?:https?://localhost:8501/)?[^)]*\.md\)",
        r"**\1**",
        content,
    )


articles = get_articles()

if not articles:
    st.warning("No Markdown knowledge articles were found in the docs folder.")
    st.stop()


# Sidebar: search settings and article browser
with st.sidebar:
    st.header("Search settings")

    result_limit = st.slider(
        "Maximum source articles",
        min_value=1,
        max_value=5,
        value=3,
    )

    st.caption(f"{len(articles)} Markdown article(s) loaded.")

    st.divider()
    st.header("Browse knowledge articles")

    article_titles = sorted(article["title"] for article in articles)

    selected_title = st.selectbox(
        "Choose an article",
        ["Select an article..."] + article_titles,
    )


# Display a selected knowledge article
if selected_title != "Select an article...":
    selected_article = next(
        article
        for article in articles
        if article["title"] == selected_title
    )

    st.subheader(selected_article["title"])

    st.caption(
        f"Source file: {selected_article['path'].relative_to(ROOT)}"
    )

    st.markdown(clean_article_links(selected_article["content"]))
    st.divider()


# Search interface
question = st.chat_input(
    "Ask about account access or password reset…"
)

if question:
    with st.chat_message("user"):
        st.write(question)

    results = search_articles(
        question,
        articles,
        limit=result_limit,
    )

    with st.chat_message("assistant"):
        if not results:
            st.write(
                "I couldn't find a relevant answer in the available "
                "documentation. Try different keywords or check whether "
                "the knowledge articles cover this topic."
            )
        else:
            st.write(
                "I found these relevant documentation sources:"
            )

            for score, article, matched_terms in results:
                with st.expander(
                    f"{article['title']} — match score {score:.0%}",
                    expanded=True,
                ):
                    st.caption(
                        f"Source file: {article['path'].relative_to(ROOT)}"
                    )

                    st.caption(
                        "Matched terms: "
                        + ", ".join(sorted(matched_terms))
                    )

                    st.markdown("**Retrieved documentation**")
                    st.markdown(
                        clean_article_links(article["content"])
                    )
