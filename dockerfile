FROM 3.11-alpine3.19

WORKDIR /usr/src/app 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 5000 

CMD ["python", "sgpools.py"]