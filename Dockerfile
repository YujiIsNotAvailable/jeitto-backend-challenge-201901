from python:3.9
  WORKDIR /app
  COPY . /app

  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt

  EXPOSE 5000
  CMD ["python3", "server.py"]