import streamlit as st
from user import User
import re
import time

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.header("Навигация")
    st.sidebar.page_link("main.py", label="Загрузить чек")
    st.sidebar.page_link("pages/account.py", label="Личный кабинет")
    st.sidebar.page_link("pages/friends.py", label="Друзья")
    st.sidebar.page_link("pages/history.py", label="История")



def unauthenticated_menu():
    with st.sidebar:
        st.header("Авторизация")
        if st.button("Войти", key="login"):
            account_login()
        st.markdown("---")
        st.header("Регистрация")
        # Кнопка "Зарегистрироваться" с popover (имитируется через st.expander)
        if st.button("Зарегистрироваться", key="register"):
            with st.expander("Регистрация", expanded=True):
                account_registration()

        st.markdown("---")
        st.header("Навигация")
        st.sidebar.page_link("main.py", label="Загрузить чек")
        st.sidebar.page_link("pages/account.py", label="Личный кабинет")
        st.sidebar.page_link("pages/friends.py", label="Друзья")
        st.sidebar.page_link("pages/history.py", label="История")


def menu():
    if "user" not in st.session_state or st.session_state.user.id is None:
        unauthenticated_menu()
        return
    else:
        authenticated_menu()
        return


@st.dialog("Вход")
def account_login():
    mail = st.text_input(label="Введите вашу почту", placeholder="example@mail.com")
    if st.button("Подтвердить вход"):
        if not re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', mail):
            st.warning('Вы ввели некорректную или несуществующую почту, проверьте ввод.', icon="⚠️")
            return

        if not User.exists_in_data_base(mail=mail):
            st.warning('Данной почты нет в базе данных. Пожалуйста, зарегистрируйтесь.', icon="⚠️")
            return

        st.session_state.user = User.get_by_mail(mail=mail)
        st.success('Вход выполнен успешно!', icon="✅")
        time.sleep(1)
        st.rerun()

@st.dialog("Регистрация")
def account_registration():
    mail = st.text_input(label="Введите вашу почту", placeholder="example@mail.com")
    if st.button("Подтвердить регистрацию"):
        if not re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', mail):
            st.warning('Вы ввели некорректную или несуществующую почту, проверьте ввод.', icon="⚠️")
            return

        if User.exists_in_data_base(mail=mail):
            st.warning('Аккаунт с данной почтой уже существует. Пожалуйста, введите другую почту.', icon="⚠️")
            return

        st.session_state.user = User(mail=mail)
        st.session_state.user.add_to_data_base()
        st.success('Регистрация прошла успешно!', icon="✅")
        time.sleep(1)
        st.rerun()

