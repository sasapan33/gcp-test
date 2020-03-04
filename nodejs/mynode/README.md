## 連線到cloudsql tips
連線方式詳見cloudsql.js

db連線參數寫在`.env`中，此處就不commit上來

不過格式大概如下

```
DB_HOST=127.0.0.1
DB_DATABASE=dbname
DB_USER=dbuser
DB_PASS=db password
```
>比較需要提的是，這裡連線是透過`cloud_sql_proxy`去連線，因此ip固定填`127.0.0.1`就可以了

若你要直接連過去，不透過cloud_sql_proxy，則要填寫cloudSQL的public ip即可

（當然cloudSQL的地方也要設定做相關設定，此處不贅述）

ps.此處使用`cloud_sql_proxy`的原因是因為我cloudSQL有開SSL，若不使用cloud_sql_proxy，則還要處理ssl的設定ＸＤ（偷懶）
