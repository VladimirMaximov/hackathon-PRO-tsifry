FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    add-apt-repository ppa:alex-p/tesseract-ocr -y && \
    apt-get update && \
    apt-get install -y \
      tesseract-ocr \
      tesseract-ocr-rus \
      libgl1-mesa-glx \
      python3-pip \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]