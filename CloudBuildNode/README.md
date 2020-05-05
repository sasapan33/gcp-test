# Cloud Build

## 環境
run一個node express的Hello World
用webpack Build

## 流程
推code[1] → Source Repositories[2] → trigger Cloud Build[3] → push to Container Registry[4] → kubectl set image(rolling update)[5]

## 事前設定
> 請先確認你所在的環境可以使用gcloud指令。<br>
> 若無法使用請參考 https://cloud.google.com/sdk/docs/initializing?hl=zh-tw 去做設定<br>
> 或可以直接使用cloud shell做你的環境也可以。

須先開啟一個GKE cluster，可利用 deploy1.yaml 直接作部署
參考語法(當然也可以直接到console去點點點做設定)
```
#create cluster
gcloud container clusters create "YOUR_CLUSTER_NAME" --region "YOUR_REGION" \
  --machine-type "g1-small" --num-nodes "1" --enable-ip-alias
```

完成後就可以透過 deploy1.yaml 去部署pod
記得部署後要expose
參考語法
```
#grant權限後才能用kubectl指令
gcloud container clusters get-credentials YOUR_CLUSTER_NAME

kubectl create -f deploy1.yaml
kubectl expose deployment hello-cloud-build-1 \
  --type=LoadBalancer --port 3000 --target-port 3000
```

--------
## 步驟
這裡步驟會對應到流程中的1/2/3/4/5
說明如下

### [1] 推code ###
把這個repo的程式通通推進Source Repositories
```
#create repo
gcloud source repos create hello-cloudbuild-app

#git init
git remote add google \
    "https://source.developers.google.com/p/YOUR_PROJECT_ID/r/hello-cloudbuild-app"

git add .
git commit -m "xx"
git push google master:master
```

### [2] Source Repositories ###
去你專案內的source repositories，看有沒有剛剛推上去的專案

### [3] trigger Cloud Build ###
到console的 `Cloud Build > Triggers` 去create一個trigger
- 設定 `push to a branch`
- 設定repo
- 設定branch
- 設定Build configuration: yaml檔位置

設定完後請存檔

### [4] push to Container Registry ###
根據cloudbuild.yaml檔來打包及部署
這個yaml檔中共有五個步驟(step)：
- npm install
- npm build(利用webpack)
- docker build
- docker push
- kubectl set image
詳細可以看yaml檔內容，記得把yaml檔裡面的一些變數改掉嘿～

yaml檔參數的詳細說明可以看這裡 https://cloud.google.com/cloud-build/docs/build-config

### [5] kubectl set image ###
然後就更新好了啊

<h2>做完了</h2>

快去再推一個code看看！