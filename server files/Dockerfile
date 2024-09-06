FROM python:3.9-slim
WORKDIR /exampledir
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 1
CMD ["python", "app.py"]