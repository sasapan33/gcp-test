# Cloud Function test

## 利用gcloud做deploy
利用gcloud指令做deploy
trigger的地方是指定這個cloud function是如何驅動的，這個指令必須在 `main.py`同一層的路徑才能執行
```
gcloud functions deploy ${main.py裡面的function name} 
  --runtime python37 
  --trigger-resource ${bucket_name} --trigger-event google.storage.object.finalize #trigger by bucket
  --trigger-http --allow-unauthenticated #trigger by http
  --region ${region_name} 
  --set-env-vars FOO=abc
```

## Cloud Function security
若由上方指令deploy上去的cloud funtion，default是對allUser全開，即只要知道endpoint就可以invoke該function。
若想要做到cloud function不裸奔，其實步驟很簡單：
- 只需要設定一個service account，讓該service account可以invoke指定的cloud function
- 在呼叫cloud function前，先帶著該service account先去一個專門驗籤的網址，取回jwt
- 呼叫cloud function時，將jwt帶進header中即可
（詳情可參考 python/GCF/Helloworld_FuncFramwork/main.py 中 triggerByPubsub.getToken()




