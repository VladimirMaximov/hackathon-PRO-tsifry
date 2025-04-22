import pandas as pd
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
            label="Разделение",
            options=["Автоматически", "Равные суммы", "Вручную"],
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
            label="Количество гостей",
            min_value=1,
            step=1,
            value=5,
            label_visibility="collapsed"
        )

    # 4. Три колонки: "Скидка:" текст, числовой input, выпадающий список с "%" и "руб."
    col1, col2, col3 = st.columns(3, vertical_alignment="center")
    with col1:
        st.markdown("**Скидка:**")
    with col2:
        discount_value = st.number_input(
            label="Скидка",
            min_value=0.0,
            step=5.,
            value=0.0,
            key=1,
            label_visibility="collapsed"
        )
    with col3:
        discount_unit = st.selectbox(
            label="Вариант",
            options=["%", "руб."],
            index=0,
            key=2,
            label_visibility="collapsed"
        )

    # 5. Три колонки: "Чаевые:" текст, числовой input, выпадающий список с "%" и "руб."
    col1, col2, col3 = st.columns(3, vertical_alignment="center")
    with col1:
        st.markdown("**Чаевые:**")
    with col2:
        tip_value = st.number_input(
            label="Чаевые",
            min_value=0.0,
            step=5.,
            value=0.0,
            key=3,
            label_visibility="collapsed"
        )
    with col3:
        tip_unit = st.selectbox(
            label="Вариант",
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

            if split_type == "Автоматически":
                st.session_state.dfs = split_automatic(guest_count)
            elif split_type == "Равные суммы":
                st.session_state.dfs = split_equal(guest_count)
            else:
                st.session_state.dfs = [pd.DataFrame({"Наименование": [],
                                                      "Количество": [],
                                                      "Цена за 1 шт.": [],
                                                      "Цена": []}) for _ in range(guest_count)]
                st.session_state.rest_dishes = st.session_state.df.copy()
                st.rerun()

            distributed = pd.concat(st.session_state.dfs, ignore_index=True)

            distributed = (
                distributed
                .groupby(["Наименование", "Цена за 1 шт."], as_index=False)
                .agg({"Количество": "sum"})
            )

            distributed["Цена"] = (
                    distributed["Количество"] * distributed["Цена за 1 шт."]
            )

            main_tuples = st.session_state.df.apply(lambda row: tuple(row), axis=1)
            distributed_tuples = distributed.apply(lambda row: tuple(row), axis=1)

            st.session_state.rest_dishes = st.session_state.df[main_tuples.isin(distributed_tuples)].reset_index(drop=True)

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


def split_automatic(guest_count: int) -> list[pd.DataFrame]:
    """
    Разбивает каждую «единицу» позиции по очереди между гостями:
      - если количество – целое N, создаёт N кусков по 1 шт.
      - и, если есть дробная часть, ещё один кусок с этим остатком.
    Порождает список dfs длины guest_count, заполняет их жадно по минимальной сумме.
    """
    cols = ["Наименование", "Количество", "Цена за 1 шт.", "Цена"]
    dfs = [pd.DataFrame(columns=cols) for _ in range(guest_count)]
    totals = [0.0] * guest_count

    for _, row in st.session_state.df.iterrows():
        name = row["Наименование"]
        qty = float(row["Количество"])
        price_unit = float(row["Цена за 1 шт."])

        # Сколько целых единиц
        int_units = int(qty)
        # Дробная часть (если есть)
        frac_unit = qty - int_units

        # 1) Раздаём по 1 шт. int_units раз
        for _ in range(int_units):
            # гость с наименьшей текущей суммой
            idx = totals.index(min(totals))
            new_row = {
                "Наименование":    name,
                "Количество":      1.0,
                "Цена за 1 шт.":   price_unit,
                "Цена":            price_unit * 1.0
            }
            dfs[idx] = pd.concat([dfs[idx], pd.DataFrame([new_row])], ignore_index=True)
            totals[idx] += price_unit

        # 2) Если осталась дробная часть – раздаём её одним куском
        if frac_unit > 0:
            idx = totals.index(min(totals))
            new_row = {
                "Наименование":    name,
                "Количество":      frac_unit,
                "Цена за 1 шт.":   price_unit,
                "Цена":            price_unit * frac_unit
            }
            dfs[idx] = pd.concat([dfs[idx], pd.DataFrame([new_row])], ignore_index=True)
            totals[idx] += price_unit * frac_unit

    return dfs


def split_equal(guest_count: int) -> list[pd.DataFrame]:
    """
        Делит каждую позицию поровну между всеми гостями.
        Берёт исходник из st.session_state.df.
        """
    cols = ["Наименование", "Количество", "Цена за 1 шт.", "Цена"]
    dfs = [pd.DataFrame(columns=cols) for _ in range(guest_count)]

    for _, row in st.session_state.df.iterrows():
        q_per = row["Количество"] / guest_count
        price_per = row["Цена за 1 шт."]
        for i in range(guest_count):
            dfs[i] = pd.concat([
                dfs[i],
                pd.DataFrame([{
                    "Наименование": row["Наименование"],
                    "Количество": q_per,
                    "Цена за 1 шт.": price_per,
                    "Цена": q_per * price_per
                }])
            ], ignore_index=True)

    return dfs
