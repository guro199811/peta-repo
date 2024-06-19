FROM python:3.10.12
WORKDIR /app

EXPOSE 5000

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./backend .

# App runs from /entrypoint
ENTRYPOINT [ "/entrypoint.sh" ]