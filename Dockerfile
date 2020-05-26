FROM python:3.8-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers make
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "./launcher.py"]