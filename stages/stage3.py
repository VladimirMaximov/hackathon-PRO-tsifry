import streamlit as st
from menu import menu


def renderStage3():
    # 1. Заголовок Markdown
    st.markdown("# Заполните дополнительную информацию")
    st.markdown("---")

    # 2. Две колонки: текст и выпадающий список "Тип разделения:"
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.markdown("**Тип разделения:**", )
    with col2:
        split_type = st.selectbox(
            label="",
            options=["Автоматически", "равные суммы", "вручную"],
            index=0,
            label_visibility="collapsed",
            placeholder="Выберите тип разделения"
        )

    # 3. Две колонки: "Количество гостей:" и числовой input
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.markdown("**Количество гостей:**")
    with col2:
        guest_count = st.number_input(
            label="",
            min_value=1,
            step=1,
            value=1,
            label_visibility="collapsed"
        )


    # 4. Три колонки: "Скидка:" текст, числовой input, выпадающий список с "%" и "руб."
    col1, col2, col3 = st.columns(3, vertical_alignment="center")
    with col1:
        st.markdown("**Скидка:**")
    with col2:
        discount_value = st.number_input(
            label="",
            min_value=0.0,
            step=5.,
            value=0.0,
            key=1,
            label_visibility="collapsed"
        )
    with col3:
        discount_unit = st.selectbox(
            label="",
            options=["%", "руб."],
            index=0,
            key=2,
            label_visibility = "collapsed"
        )


    # 5. Три колонки: "Чаевые:" текст, числовой input, выпадающий список с "%" и "руб."
    col1, col2, col3 = st.columns(3, vertical_alignment="center")
    with col1:
        st.markdown("**Чаевые:**")
    with col2:
        tip_value = st.number_input(
            label="",
            min_value=0.0,
            step=5.,
            value=0.0,
            key=3,
            label_visibility="collapsed"
        )
    with col3:
        tip_unit = st.selectbox(
            label="",
            options=["%", "руб."],
            index=0,
            key=4,
            label_visibility="collapsed"
        )


    # 6. Две колонки: "Добавить друзей:" текст, и кнопка "Добавить"
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.markdown("**Добавить друзей:**")
    with col2:
        add_friend = st.button("Добавить", use_container_width=True)


    # 7. Две колонки: кнопки "Назад" и "Далее"
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        if st.button("Назад", use_container_width=True):
            st.session_state.stage = 2
            st.rerun()

    with col2:
        if st.button("Далее", use_container_width=True):
            st.session_state.stage = 4
            st.rerun()

    menu()
    # Можно вернуть значения для дальнейшей обработки, если необходимо
    st.session_state.more_info = {
        "split_type": split_type,
        "guest_count": guest_count,
        "discount_value": discount_value,
        "discount_unit": discount_unit,
        "tip_value": tip_value,
        "tip_unit": tip_unit,
        "add_friend": add_friend
    }