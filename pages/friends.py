import streamlit as st
from menu import menu


class FriendsPage:
    def __init__(self):
        pass

    @staticmethod
    def render():
        st.set_page_config(
            page_title="СберЧек - список друзей",  # Отображаемый заголовок вкладки
            page_icon=":busts_in_silhouette:"  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
        )
        st.title("Друзья")
        st.write("Здесь будет информация о друзьях пользователя.")

        menu()


FriendsPage.render()
