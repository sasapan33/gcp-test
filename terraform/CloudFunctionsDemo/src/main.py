from google.cloud import storage
import os

def sasa_http_sample(request):
    print('sasa_http_sample=', request)
    request_json = request.get_json(silent=True)
    request_args = request.args

    filename = ''
    if request_args and 'filename' in request_args:
        filename = request_args['filename']
    elif request_json and 'filename' in request_json:
        filename = request_json['filename']

    if filename != '' :
        print('start moving to backup!', filename)
        storage_client = storage.Client(project=os.environ['PROJECT_ID'])

        src_bucket = storage_client.bucket(os.environ['SRC_BUCKET'])
        dist_bucket = storage_client.bucket(os.environ['DIST_BUCKET'])

        blob = src_bucket.blob(filename)
        new_blob = src_bucket.copy_blob(blob, dist_bucket)
        new_blob.acl.save()
        print("copy success")

        src_bucket.delete_blob(filename)
        print("delete success")
    
