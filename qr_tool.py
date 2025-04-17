import qrcode
from PIL import Image

def gen_qr_code(phone_number : str) -> Image:
    """Функция для получения QR-кода на оплату
    """

    # Ссылка в окно перевода сбербанка  
    url = f"https://www.sberbank.com/sms/pbpn?requisiteNumber={phone_number}"

    # создание QR-кода, хранящего заданную ссылку
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    return qr_img


if __name__ == "__main__":
    qr_img = gen_qr_code("71111111111")
    qr_img.show()
    
