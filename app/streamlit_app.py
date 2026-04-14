import streamlit as st


st.set_page_config(
    page_title="Argentina vs France — World Cup Final 2022",
    layout="wide",
)

st.title("Argentina vs France — World Cup Final 2022")
st.subheader("Portfolio project in progress")

st.markdown(
    """
This repository already contains the full notebook analysis of the 2022 World Cup Final.

The next step is to turn that work into a Streamlit application with:
- a match story,
- tactical team analysis,
- player profiles,
- and interactive visuals.
"""
)

st.info(
    "Notebook analysis is ready. Streamlit V1 is the next milestone for this project."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Current project assets")
    st.markdown(
        """
- 4 completed notebooks
- processed and raw datasets
- exported figures
- tactical and player-level commentary
"""
    )

with col2:
    st.markdown("### Planned app sections")
    st.markdown(
        """
- Match overview
- Team tactical analysis
- Player analysis
- Key insights
- Methodology
"""
    )
