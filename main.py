import streamlit as st
from pages.account import AccountPage
from pages.history import HistoryPage
from pages.friends import FriendsPage
from menu import menu
from user import User


class MainPage:
    def __init__(self):
        pass

    @staticmethod
    def render():
        st.set_page_config(
            page_title="СберЧек - главная",  # Отображаемый заголовок вкладки
            page_icon=":bank:",  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
            layout="wide"
        )

        st.markdown("# СберЧек - разделение счета по фотографии чека")

        st.image("test_photo2.jpg",)

        if st.button("Загрузить фото чека"):
            st.write("Функция загрузки фото чека активирована!")

        menu()


if "user" not in st.session_state:
    st.session_state.user = User()

MainPage().render()

