FROM python:latest

WORKDIR /google_map_api

COPY . /google_map_api

RUN pip3 install -r requirements.txt

CMD ["python", "google_map_api_method/api_method.py"] 
