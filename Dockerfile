FROM python:3.7.1-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY gbdx_catalog_search.py .

CMD [ "python3", "./gbdx_catalog_search.py" ]
EXPOSE 5000
