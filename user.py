import pandas as pd


"""Класс Person реализует объект-аккаунт человека"""
class User:
    def __init__(self, id=None, full_name=None, mail=None, phone_number=None):
        self.id = id
        self.full_name = full_name
        self.mail = mail
        self.phone_number = phone_number

    def set_full_name(self, full_name: str):
        self.full_name = full_name

    def set_mail(self, mail: str):
        self.mail = mail

    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number

    def __repr__(self):
        return f"User(id={self.id}, full_name={self.full_name}, phone_number={self.phone_number})"

    @staticmethod
    def exists_in_data_base(mail: str) -> bool:
        """
        Проверяет, содержится ли в файле запись с заданной почтой.
        Возвращает True, если такая запись существует, иначе False.
        """
        df = pd.read_excel("data/users.xlsx")
        return not df[df["mail"] == mail].empty


    def add_to_data_base(self):
        """
        Добавляет текущего пользователя в файл Excel.
        Если запись с такой почтой уже существует, выбрасывает ValueError.
        Новому пользователю присваивается id, равный (max(id) + 1).
        """
        df = pd.read_excel("data/users.xlsx", )
        if not df[df["mail"] == self.mail].empty:
            raise ValueError("Пользователь с такой почтой уже существует!")

        # Определяем новый id
        if df.empty:
            new_id = 1
        else:
            # Если столбец "id" имеет числовой тип, находим максимальное значение
            new_id = int(df["id"].max()) + 1
        self.id = new_id

        # Создаем новую строку в виде DataFrame
        new_row = pd.DataFrame([{
            "id": self.id,
            "full_name": self.full_name,
            "mail": self.mail,
            "phone_number": self.phone_number
        }])
        # Объединяем с уже существующими данными
        df = pd.concat([df, new_row], ignore_index=True)

        df.to_excel("data/users.xlsx", index=False)


    @staticmethod
    def delete_from_data_base(mail: str):
        """
        Удаляет запись с заданной почтой из файла Excel.
        Если запись с такой почтой не найдена, выбрасывает ValueError.
        """
        df = pd.read_excel("data/users.xlsx")
        if df[df["mail"] == mail].empty:
            raise ValueError("Пользователь с такой почтой не найден!")
        # Оставляем только те записи, у которых почта не равна заданной
        df = df[df["mail"] != mail]

        df.to_excel("data/users.xlsx", index=False)

    @classmethod
    def get_by_mail(cls, mail: str) -> "User":
        """
        Ищет в файле users.xlsx запись с заданной почтой и возвращает объект User с данными из этой строки.
        Предполагается, что пользователь с данной почтой точно существует.
        """
        df = pd.read_excel("data/users.xlsx")
        # Фильтрация строк, где столбец mail соответствует переданной почте.
        filtered = df[df["mail"] == mail]
        if filtered.empty:
            raise ValueError(f"Пользователь с почтой {mail} не найден!")
        # Берем первую найденную запись (должна быть только одна, если почта уникальна)
        row = filtered.iloc[0]
        return cls(
            id=row["id"],
            full_name=row["full_name"],
            mail=row["mail"],
            phone_number=row["phone_number"]
        )
