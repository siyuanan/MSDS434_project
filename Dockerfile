FROM python:3

RUN mkdir -p /app
COPY . /app/
WORKDIR /app
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3"]
# CMD ["main.py"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
