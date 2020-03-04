# gcp-test
需設定環境變數讓gcp認識你是誰

https://cloud.google.com/docs/authentication/getting-started

記得credential不要上傳
透過以下方式宣告

```
export GOOGLE_APPLICATION_CREDENTIALS=XXX.json
```

-------

## Access cloudSQL
記得宣告以下參數
```
export CLOUD_SQL_CONNECTION_NAME='<MY-PROJECT>:<INSTANCE-REGION>:<INSTANCE-NAME>'
export DB_USER='my-db-user'
export DB_PASS='my-db-pass'
export DB_NAME='my_db'
```

##### 會用到的套件
```
sqlalchemy
pymysql
```