# gcp-test

## python
目前sample有：111
- list/create instance
- list all bucket
- insert/list cloudsql 某一個table的東西
- cloud function相關

需設定環境變數讓gcp認識你是誰

https://cloud.google.com/docs/authentication/getting-started

記得credential不要上傳
透過以下方式宣告

```
export GOOGLE_APPLICATION_CREDENTIALS=${XXX.json}
```

### Access cloudSQL
記得宣告以下參數
```
export CLOUD_SQL_CONNECTION_NAME='${projectname}:${region}:${sql instance name}'
export DB_USER='${db-user-name}'
export DB_PASS='${db-password}'
export DB_NAME='${db-name}'
```

**會用到的套件**
```
sqlalchemy
pymysql
```
-------
## nodejs
目前sample有：
- insert/list cloudsql 某一個table的東西

### Access cloudSQL
連線方式詳見cloudsql.js

db連線參數寫在`.env`中，此處就不commit上來

不過格式大概如下

```
DB_HOST=127.0.0.1
DB_DATABASE=dbname
DB_USER=dbuser
DB_PASS=db password
```
-------
### 關於cloudSQL的連線方式
這裡連線是透過`cloud_sql_proxy`去連線，因此ip固定填`127.0.0.1`就可以了

附上開proxy相關語法

```
cloud_sql_proxy -instances=${project_id}:${region}:${sql instance name}=tcp:3306 -credential_file=${json}
```

若你要直接連過去，不透過cloud_sql_proxy，則要填寫cloudSQL的public ip即可

當然cloudSQL的地方也要設定做相關設定，此處不贅述

ps.此處使用`cloud_sql_proxy`的原因是因為我cloudSQL有開SSL，若不使用cloud_sql_proxy，則還要處理ssl的設定ＸＤ
