﻿


# СберЧек

Реализация приложения для деления счета разработанного в рамках всероссийского кейс-чемпионата ProЦифру.  Целью проекта была разработка сервиса, который с помощью технологии оптического распознавания символов (OCR) автоматически извлекает данные с бумажного чека ресторана и предлагает удобные варианты деления счета между участниками.

## Содержание

-   Описание
    
-   Технологии
    
-   Использование
    
-   Архитектура

-   Модули и компоненты
    
-   Помочь проекту
    
-   Контакты
    
## Описание

СберЧек — интерактивное приложение для автоматического и ручного разделения ресторанного счета по фотографии чека. Пользователь загружает изображение чека, редактирует распознанные позиции, указывает параметры разделения (количество гостей, скидки, чаевые), и получает готовые суммы к оплате с возможностью генерации QR‑кодов.

## Технологии

Перечислите основные технологии и версии:

-   Python
    
-   Tesseract
    
-   Streamlit

-   pandas
    
-   Pillow
    
-   qrcode

## Использование


1.  **Вход в приложение по [ссылке](https://sbercheck.streamlit.app/)**

2. **Загрузка чека**: на главной странице загрузите изображение чека.
    
3.  **Редактирование позиций**: при необходимости отредактируйте количество и цены в таблице.
    
4.  **Дополнительные параметры**: выберите тип разделения (автоматически, равные суммы или вручную), укажите количество гостей, скидки, чаевые, добавьте друзей.
    
5.  **Итоги**: приложение рассчитает сумму для каждого участника и сгенерирует QR‑коды для оплаты.
    
6.  **Авторизация**: зарегистрируйтесь или войдите в личный кабинет для сохранения истории и работы с друзьями.

## Архитектура

```
.
├── .streamlit           # Конфигурация Streamlit (стили, тема)
├── data                 # Данные пользователей (users.xlsx)
├── OCR                  # Модель и скрипт распознавания и классификации позиций чека
├── pages                # Страницы приложения (аккаунт, друзья, история)
├── stages               # Основные этапы обработки (загрузка, редактирование, параметры, результат)
├── menu.py              # Логика бокового меню и диалогов регистрации/входа
├── main.py              # Точка входа и маршрутизация этапов
├── qr_tool.py           # Генерация QR‑кодов для оплаты
├── user.py              # Класс User для работы с базой данных (Excel)
└── test_photo*.jpg      # Изображение для приветственного экрана
```
([github.com](https://github.com/VladimirMaximov/hackathon-PRO-tsifry/tree/main))

 ## Модули и компоненты

-   **main**: конфигурация и переход между этапами работы приложения.
    
-   **menu**: авторизация (вход/регистрация) и навигация.
    
-   **qr_tool**: генерация QR‑кода платежа.
    
-   **user**: управление данными пользователей в Excel.
    
-   **stages/**: четыре этапа (`stage1.py` – загрузка, `stage2.py` – редактирование, `stage3.py` – параметры, `stage4.py` – результаты).
    
-   **pages/**: вспомогательные страницы (личный кабинет, друзья, история).
    
-   **OCR/**: модель классификации позиций чека (файл `best_model.joblib` и скрипт `for_classifier.`

## Помочь проекту

1.  Создайте форк репозитория
    
2.  Создайте новую ветку: `git checkout -b feature/имя-ветки`
    
3.  Сделайте изменения и закоммитьте: `git commit -m "Добавляет новую фичу"`
    
4.  Запушьте ветку и создайте Pull Request
    
##  Контакты

- **Максимов Владимир** — [GitHub](https://github.com/VladimirMaximoм)
- **Авраменко Артемий** — [GitHub](https://github.com/ArtemiyAvramenko)
- **Корягин Кирилл** — [GitHub](https://github.com/gr0w1)
- **Фёдоров Роман** — [GitHub](https://github.com/RomanFyo )
- **Артамонова Анфиса** — [GitHub](https://github.com/anfisartamonova)
    

