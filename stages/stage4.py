import streamlit as st
from menu import menu
import pandas as pd


def renderStage4(dfs: [pd.DataFrame]):
    st.session_state.final_dfs = []

    for i in range(1, st.session_state.more_info["guest_count"] + 1):
        with st.expander(f"Гость {i}"):
            st.session_state.final_dfs.append(st.data_editor(dfs[i-1], num_rows="dynamic", key=i))



    menu()