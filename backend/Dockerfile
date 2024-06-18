FROM python:3.10.12
WORKDIR /app

EXPOSE 5000

COPY ./backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./backend .


CMD python3 -m flask --app ./backing-pet/main.py run --host=0.0.0.0