from google.cloud import storage

def list_bucket():
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket, '====')
        blobs = storage_client.list_blobs(bucket.name)
        
        for blob in blobs:
            print(blob.name)

list_bucket()