import cv2

import numpy as np

from PIL import Image

import pytesseract

import re

from thefuzz import fuzz

from sklearn.linear_model import LogisticRegression

import joblib

import pandas as pd

# from sentence_transformers import SentenceTransformer


def remove_shadow(image):
    if len(image.shape) == 3:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    else:

        gray = image.copy()

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))

    dilated = cv2.dilate(gray, kernel)

    bg = cv2.medianBlur(dilated, 21)

    diff = cv2.absdiff(gray, bg)

    norm_img = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return norm_img


def ocr_on_preprocessed_image(image_path, config=r'--oem 1 --psm 6'):
    image = image_path

    # Предварительная обработка изображения

    processed_img = remove_shadow(image)

    # Конвертация изображения из OpenCV (numpy.ndarray) в формат, совместимый с PIL

    pil_img = Image.fromarray(processed_img)

    data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)

    # Распознавание текста с помощью pytesseract

    text = pytesseract.image_to_string(pil_img, lang='rus', config=config + ' -c preserve_interword_spaces=1')

    return text


def merge_numbers(text):
    return re.sub(r'(\d+)\s+(\d+)$', r'\1\2', text)


def merge_strings(arr):
    result = []

    current_str = []

    for item in arr:

        if isinstance(item, str):

            current_str.append(item)


        else:

            if current_str:
                result.append(' '.join(current_str))

                current_str = []

            result.append(item)

    if current_str:
        result.append(' '.join(current_str))

    return result


def merge_arrays(arr):
    result = [['']]

    for i in range(len(arr)):

        item = arr[i]

        if len(item) == 1:

            if isinstance(item[0], str):
                result[-1][0] = ' '.join([result[-1][0], item[0]])


        else:

            result.append(item)

    return result[1:]


def parse_dish(lines):
    clean_lines = []

    for line in lines:

        clean_arr = []

        for item in line:

            try:

                clean_arr.append(float(item.replace(',', '.')))


            except:

                if len(item) >= 3:
                    clean_arr.append(item)

        clean_lines.append(clean_arr)

    return [merge_strings(arr) for arr in clean_lines if arr]


def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)

    text = re.sub(r'\d+', '', text)

    return text.strip()


# def predict_dish_category(dish_name, classifier, encode_model):
#     cleaned_name = clean_text(dish_name.lower())
#
#     embedding = encode_model.encode([cleaned_name])
#
#     probs = classifier.predict_proba(embedding)[0]
#
#     categories = ['закуски', 'суп', 'горячее', 'салат', 'десерт', 'напиток']
#
#     most_probable = sorted(zip(categories, probs), key=lambda x: -x[1])[0]
#
#     return most_probable[0]


def get_result(path_img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    # classifier = joblib.load('best_model.joblib')

    recognized_text = ocr_on_preprocessed_image(path_img)

    recognized_text = merge_numbers(recognized_text)

    strings = [string for string in recognized_text.splitlines() if string]

    lines = [re.sub("[^А-Яа-я0-9,/-]", " ", string).split() for string in strings]

    prepare_dish = parse_dish(lines)

    start = 0

    end = 0

    start_token = ["наименование", "кол-во", "количество", "цена", "сумма"]

    end_token = ["итого", "итог", "к оплате", "всего"]

    for idx, group in enumerate(prepare_dish):

        try:

            for name in group[0].split():

                start_check = [fuzz.partial_token_sort_ratio(name, token) >= 85 for token in start_token]

                end_check = [fuzz.partial_token_sort_ratio(name, token) >= 85 for token in end_token]

                if any(start_check):
                    start = idx

                if any(end_check):
                    end = idx


        except:

            continue

    end = len(prepare_dish) if end == 0 else end

    result = merge_arrays(parse_dish(lines)[start + 1:end])

    result_check = []

    for arr in result:
        dict_dishes = {}

        dict_dishes['name'] = arr[0]

        dict_dishes['count'] = arr[-2]

        dict_dishes['price'] = arr[-1]

        result_check.append(dict_dishes)

    for string in result_check:

        try:

            product = string['name']

            # prediction = predict_dish_category(product, classifier, model)

            # string['category'] = prediction


        except:

            continue

    return format_result(pd.DataFrame(result_check).dropna())



def format_result(df):
    # df.drop("category", axis=1, inplace=True)
    df.columns = ["Наименование", "Количество", "Цена"]
    df.loc[:, "Цена за 1 шт."] = df["Цена"] / df["Количество"]
    return df


if __name__ == "__main__":
    print(get_result("check2.jpg"))