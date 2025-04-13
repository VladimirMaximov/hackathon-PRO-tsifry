import streamlit as st
from menu import menu

class HistoryPage:
    def __init__(self):
        pass

    @staticmethod
    def render():
        st.set_page_config(
            page_title="СберЧек - история",  # Отображаемый заголовок вкладки
            page_icon=":scroll:"  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
        )
        st.title("История")
        st.write("Здесь будет отображаться история чеков или действий пользователя.")

        menu()

HistoryPage.render()