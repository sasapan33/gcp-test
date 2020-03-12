# Cloud Function test

# 利用gcloud做deploy
利用gcloud指令做deploy
trigger的地方是指定這個cloud function是如何驅動的
```
gcloud functions deploy ${main.py裡面的function name} 
  --runtime python37 
  --trigger-resource ${bucket_name} --trigger-event google.storage.object.finalize #trigger by bucket
  --trigger-http --allow-unauthenticated #trigger by http
  --region ${region_name} 
  --set-env-vars FOO=abc
```
