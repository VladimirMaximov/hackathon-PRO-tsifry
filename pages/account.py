import streamlit as st
from menu import menu


def renderAccount():
    st.set_page_config(
        page_title="СберЧек - личный кабинет",  # Отображаемый заголовок вкладки
        page_icon=":bust_in_silhouette:"  # Необязательно: можно задать иконку (эмодзи, URL или путь к изображению)
    )
    st.title("Личный кабинет")
    st.write("Здесь будет информация о личном кабинете пользователя.")
    menu()

renderAccount()