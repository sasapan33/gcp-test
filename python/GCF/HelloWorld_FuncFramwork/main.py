import os
import requests
import json

def hello(request):
    print('hello=', request)
    return 'YAYAYA'

def slackToMe(request):
    print('hello=', request)
    request_json = request.get_json(silent=True)
    request_args = request.args

    data = 'hello cloud function!'
    if request_args and 'text' in request_args:
        data = request_args['text']
    elif request_json and 'text' in request_json:
        data = request_json['text']

    dict_headers = {'Content-type': 'application/json'}
    dict_payload = {
        "text": data}
    json_payload = json.dumps(dict_payload)

    rtn = requests.post(os.environ['SLACK_WEBHOOK'], data=json_payload, headers=dict_headers)
    print(rtn.text)

def triggerByBucket(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    print('data=', data['bucket'], '===', data['name'])
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))
    #toslack
    dict_headers = {'Content-type': 'application/json'}
    dict_payload = {
        "text": 'bucket='+data['bucket']+'中有一個上傳檔案='+data['name']}
    json_payload = json.dumps(dict_payload)
    url = os.environ['SLACKTOME']
    rtn = requests.post(url, data=json_payload, headers=dict_headers)
    print(rtn.text)

# slackToMe() os.environ['SLACK_WEBHOOK']