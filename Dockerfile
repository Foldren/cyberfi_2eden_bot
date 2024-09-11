FROM python:3.12-slim

WORKDIR /root

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./.project
#e3
CMD ["python", "bot.py"]