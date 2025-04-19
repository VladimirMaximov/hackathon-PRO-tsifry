import streamlit as st
from menu import menu
import pandas as pd
from time import sleep


def renderStage4():
    st.session_state.final_dfs = []

    for i in range(1, st.session_state.more_info["guest_count"] + 1):
        with st.expander(f"Гость {i}"):
            if "Выбрать" not in st.session_state.dfs[i - 1].columns:
                st.session_state.dfs[i - 1].insert(0, "Выбрать", False)

            st.session_state.dfs[i-1] = st.data_editor(
                st.session_state.dfs[i-1],
                disabled=st.session_state.dfs[i-1].columns.tolist()[1:],
                key=f"dataframe_{i}"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Удалить выбранное", key=f"delete_{i}", use_container_width=True):
                    move_selected_to_rest(i-1)
                    st.rerun()


            with col2:
                if st.button("Добавить позицию", key=f"add_{i}", use_container_width=True):
                    add_dish_dialog(i-1)

    col = st.columns(1)[0]
    with col:
        if st.button("Завершить", use_container_width=True, key="Finish"):
            # здесь можно сохранить финальные данные или перейти дальше
            st.session_state.stage = 5
            st.rerun()

    menu()


def move_selected_to_rest(guest_idx: int):
    """
    Переносит отмеченные чекбоксом строки из dfs[guest_idx] в rest_dishes.
    Если в rest_dishes уже есть такое наименование, суммирует количество и цену.
    """
    # 1) текущий df гостя
    df_guest: pd.DataFrame = st.session_state.dfs[guest_idx].copy()
    # 2) все отмеченные строки
    selected = df_guest[df_guest["Выбрать"]]
    if selected.empty:
        return  # ничего не выбрано
    # 3) остачный DataFrame
    rest: pd.DataFrame = st.session_state.rest_dishes.copy()
    for _, row in selected.iterrows():
        name = row["Наименование"]
        qty = row["Количество"]
        unit_price = row["Цена за 1 шт."]
        price = row["Цена"]
        if name in rest["Наименование"].values:
            # суммируем
            rest.loc[rest["Наименование"] == name, "Количество"] += qty
            rest.loc[rest["Наименование"] == name, "Цена"] += price
        else:
            # добавляем новую строку
            new_row = {
                "Наименование": name,
                "Количество": qty,
                "Цена за 1 шт.": unit_price,
                "Цена": price
            }
            rest = pd.concat([rest, pd.DataFrame([new_row])], ignore_index=True)
    # 4) удаляем отмеченные из df_guest
    df_guest = df_guest[~df_guest["Выбрать"]].drop(columns=["Выбрать"]).reset_index(drop=True)
    # 5) сохраняем результат
    st.session_state.rest_dishes = rest.reset_index(drop=True)
    st.session_state.dfs[guest_idx] = df_guest.reset_index(drop=True)


@st.dialog("Выберите одну позицию для добавления и количество", width="large")
def add_dish_dialog(guest_idx: int):
    # 1. Подготовка таблицы с чекбоксом
    df = st.session_state.rest_dishes.copy()
    if "Выбрать" not in df.columns:
        df.insert(0, "Выбрать", False)

    # 2. Выводим data_editor
    edited = st.data_editor(
        df,
        key="dialog_rest_editor",
        hide_index=True,
        use_container_width=True
    )

    # 3. Два поля: текст + ввод числа
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Введите количество:**")
    with col2:
        quantity = st.number_input(
            label="",
            min_value=0.0,
            step=0.1,
            value=0.0,
            format="%.2f",
            label_visibility="collapsed"
        )

    # 4. Кнопка «Добавить» во всю ширину
    add_col = st.columns(1)[0]
    with add_col:
        if st.button("Добавить", use_container_width=True):
            # 1) Берем только отмеченные строки
            selected = edited[edited["Выбрать"]]
            if selected.empty:
                st.info("Сначала выберите хотя бы одно блюдо.")
                return

            # 2) Работаем только с первой выбранной
            row = selected.iloc[0]
            name = row["Наименование"]
            max_qty = float(row["Количество"])
            unit_price = float(row["Цена за 1 шт."])

            # Проверки на количество
            if quantity <= 0:
                # ничего не делаем
                st.info("Количество должно быть больше нуля.")
                return
            if quantity > max_qty:
                st.warning(f"Количество не может превышать {max_qty:.2f}.")
                return

            # 3) Добавляем или обновляем в dfs[guest_idx]
            guest_df = st.session_state.dfs[guest_idx].copy()

            if name in guest_df["Наименование"].values:
                # обновляем существующую строку
                mask = guest_df["Наименование"] == name
                guest_df.loc[mask, "Количество"] += quantity
                guest_df.loc[mask, "Цена"] = guest_df.loc[mask, "Количество"] * unit_price
            else:
                # добавляем новую
                new_row = {
                    "Выбрать": False,
                    "Наименование": name,
                    "Количество": quantity,
                    "Цена за 1 шт.": unit_price,
                    "Цена": quantity * unit_price
                }
                guest_df = pd.concat([guest_df, pd.DataFrame([new_row])], ignore_index=True)

            st.session_state.dfs[guest_idx] = guest_df

            # 4) Удаляем из rest_dishes указанное количество
            rest = st.session_state.rest_dishes.copy()
            mask = rest["Наименование"] == name
            # Если количество целиком забрали — удаляем строку
            if quantity == max_qty:
                rest = rest[~mask].reset_index(drop=True)
            else:
                # иначе уменьшаем количество и цену
                rest.loc[mask, "Количество"] = rest.loc[mask, "Количество"] - quantity
                rest.loc[mask, "Цена"] = rest.loc[mask, "Количество"] * unit_price
            st.session_state.rest_dishes = rest

            st.success(f"Добавлено {quantity:.2f} шт. «{name}» гостю #{guest_idx + 1}")
            sleep(1)
            st.rerun()


