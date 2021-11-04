import streamlit as st
import numpy as np
import arxiv
from paperswithcode import PapersWithCodeClient

if 'client' not in st.session_state:
    st.session_state.client = PapersWithCodeClient()

with st.sidebar:
    """
    # Papers for search
    """
    st.markdown("<br>", unsafe_allow_html=True)
    """Read me: Steps to use 
    
    1. Type a query to search for 
    
    2. Select a paper to get more info 
    
    3. Choose option to see more
    
    ---
    """

query = st.text_input(label="search here: ")
search = arxiv.Search(
    query=query,
    max_results=3,
    sort_by=arxiv.SortCriterion.Relevance
)

if query != '':
    select = None
    title_op = []
    papers = []
    for paper in search.results():
        title_op.append(paper.title)
        papers.append(paper)
    idx = st.radio('', range(len(title_op)), format_func=lambda x: title_op[x])
    select = papers[idx]

    c1, c2, c3 = st.columns(3)
    c1.write('[' + select.title + '](' + select.pdf_url + ')')
    c2.write(select.authors[0].name)
    c3.write(select.published)
    st.write(select.summary)

    option = st.selectbox("Select option", ['author', 'git'])

    if select is not None:
        if option == 'git':
            # githubs
            papers = st.session_state.client.paper_list(q=select.title)
            if len(papers.results) > 0:
                repos = st.session_state.client.paper_repository_list(paper_id=papers.results[0].id)
                if len(repos.results) > 0:
                    for repo in repos.results:
                        st.write('code {} stars {} framework {}'.format(repo.url, repo.stars, repo.framework))
                else:
                    st.write('no code found')
            else:
                st.write('no code found')
        elif option == 'author':
            # author stats
            for i, author in enumerate(select.authors):
                st.write('author {}: {}'.format(i, author.name))
        else:
            print('select error')
            exit(1)
