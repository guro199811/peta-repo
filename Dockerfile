FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r web-files/requirements.txt
EXPOSE 5000

RUN pip install Flask-Migrate
COPY entrypoint.sh /entrypoint.sh
COPY ./web-files /app
RUN chmod +x /entrypoint.sh
# CMD ["python", "web-files/main.py"]

# ENTRYPOINT ["/entrypoint.sh"]
# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]


ENV FLASK_APP=./main.py
# ENV FLASK_DEBUG=1


CMD python3 -m flask --app ./main.py run --host=0.0.0.0
