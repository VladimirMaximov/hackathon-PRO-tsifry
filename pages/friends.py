import streamlit as st
from menu import menu


def renderFriends():
    st.set_page_config(
        page_title="СберЧек - список друзей",  # Отображаемый заголовок вкладки
        page_icon=":busts_in_silhouette:"  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
    )
    st.title("Друзья")
    st.write("Здесь будет информация о друзьях пользователя.")
    menu()


renderFriends()
