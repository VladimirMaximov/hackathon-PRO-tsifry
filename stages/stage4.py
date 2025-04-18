import streamlit as st
from menu import menu
import pandas as pd


def renderStage4():
    # st.write(st.session_state.rest_dishes)
    # st.write(st.session_state.dfs)
    # st.write(st.session_state.df)
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
                    st.write("Нажата кнопка")

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
    st.session_state.dfs[guest_idx] = df_guest