import streamlit as st
import pandas as pd
from menu import menu


def renderStage2(df: pd.DataFrame):
    # 1. Вывод заголовка в формате Markdown
    st.markdown("# Измените значения в ячейках по необходимости")

    # 2. Вывод таблицы DataFrame
    st.session_state.df = st.data_editor(df, num_rows="dynamic", hide_index=True)

    # 3. Вывод 3 кнопок в одной строке с использованием st.columns
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Назад", use_container_width=True):
            st.session_state.stage = 1
            st.rerun()
            # Здесь можно добавить логику для перехода на предыдущий этап

    with col2:
        if st.button("Посмотреть фото чека", use_container_width=True):
            st.session_state.show_photo = True
            # Здесь можно добавить логику для отображения фото чека

    with col3:
        if st.button("Далее", use_container_width=True):
            st.session_state.stage = 3
            st.rerun()
            # Здесь можно добавить логику для перехода к следующему этапу
    menu()

    if st.session_state.show_photo:
        give_photo()
        st.session_state.show_photo = False


@st.dialog("Фото чека")
def give_photo():
    st.image(st.session_state.image)