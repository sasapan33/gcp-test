import os
import requests
import json
import base64

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
    print('triggerByBucket=', data['bucket'], '===', data['name'])
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    #toslack
    dict_headers = {'Content-type': 'application/json'}
    dict_payload = {
        "text": 'bucket='+data['bucket']+'中有一個上傳檔案='+data['name']}
    json_payload = json.dumps(dict_payload)
    url = os.environ['SLACKTOME']
    rtn = requests.post(url, data=json_payload, headers=dict_headers)
    print(rtn.text)

def triggerByPubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    

    def getToken():
        func_url = os.environ['SLACKTOME']
        metadata_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

        token_url = metadata_url + func_url
        token_header = {'Metadata-Flavor': 'Google'}

        token_response = requests.get(token_url, headers=token_header)
        jwt = token_response.content.decode('utf-8')
        print('jwt===',jwt)
        return jwt
        

    print("triggerByPubsub {} published at {}".format(context.event_id, context.timestamp))

    if 'data' in event:
        jwt = getToken()

        name = base64.b64decode(event['data']).decode('utf-8')
        #toslack
        dict_headers = {'Content-type': 'application/json', 'Authorization': f'bearer {jwt}'}
        dict_payload = {
            "text": 'pubsub來了一個訊息='+name
        }
        json_payload = json.dumps(dict_payload)
        url = os.environ['SLACKTOME']
        rtn = requests.post(url, data=json_payload, headers=dict_headers)
        print(rtn.text)
    else:
        name = 'no data'
    print('Hello {}!'.format(name))

# slackToMe() os.environ['SLACK_WEBHOOK']
