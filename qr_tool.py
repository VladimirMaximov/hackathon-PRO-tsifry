import qrcode
from io import BytesIO

def gen_qr_code(phone_number: str) -> bytes:
    """Генерация QR‑кода в байтах PNG."""
    url = f"https://www.sberbank.com/sms/pbpn?requisiteNumber={phone_number}"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)

    # Получаем PIL‑изображение
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраняем в буфер и возвращаем байты
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


if __name__ == "__main__":
    qr_img = gen_qr_code("71111111111")
    qr_img.show()
    
