# USE terraform to build Cloud Functions
最近玩了一下terraform，分享些入門的東西

這folder主要是demo用terraform去部署Cloud Functions

Cloud Functions有兩隻，功能簡述如下：
- 一隻是trigger http直接用https方式呼叫的
- 另外一隻是trigger by bucket然後把bucket中的csv檔丟進bq，做完後，會把bq_job_id通知pubsub

## 目錄結構

```
--- root
 |-- generated
 |-- src
   |-- main.py
   |-- requirements.txt
 |-- terraform
   |-- main.tf
   |-- terraform.tfvars
   |-- vairables.tf
```

Cloud Functions source code放在src裡面（ `src`這個名稱可以隨便取）
裡面一定要有一個主程式`main.py` 及 安裝檔`requirements.txt `

terraform folder裡面放的就是terraform的宣告
- `main.tf` 裡面放的是terraform要做的事情，若有多項要做的，會平行處理
- `variables.tf` main.tf裡面若有要使用一些變數，要在這裡先在宣告，宣告變數的型態（或給預設值）
- `terraform.tfvars` 從這裡給予值可依環境設定不同參數，這樣比較方便

＊在terraform裡面還是要宣告要使用的credential，因為如果是在本機，並不會直接使用gcloud裡面的credential

## deploy
```
terraform init
terraform apply
```

## reference
https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function#https_trigger_url
