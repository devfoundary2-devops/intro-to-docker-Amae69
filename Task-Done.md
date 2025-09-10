### **Task Done**
---
- Modified **app.py** file Where i wrap the connection in a try/except and also add proper error handling for get/set.

- Modified **docker-compose.yaml** file to add redis service as it only has app and postgres dp

- Also I modified **requirements.txt** file to include redis and psycopg2-binary

- Run `docker-compose up -d --build` to build the app, redis, and postgress db

- Run `docker ps` to see the running app

![](./images/dockerps%201.png)

- Run: `curl http://localhost:8080/` to confirm my app running

![curl app](./images/curl%20app.png)

- Run : `curl http://localhost:8080/db-test` to test my postgres db

![curl db](./images/curl%20db.png)