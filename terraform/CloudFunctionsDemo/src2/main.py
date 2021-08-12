from google.cloud import bigquery
from google.cloud import pubsub_v1
import os
import json


def bq_load_job(data, context):
    """
    load job
    """
    print('triggerByBucket=', data['bucket'], '===', data['name'])
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    
    if (data['name'] and data['name'].find('.csv')>-1) :

        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("department", "STRING")
            ],
            skip_leading_rows=1,
            # The source format defaults to CSV, so the line below is optional.
            source_format=bigquery.SourceFormat.CSV,
        )
        uri = "gs://"+data['bucket']+"/"+data['name']

        client = bigquery.Client()
        load_job = client.load_table_from_uri(
            uri, os.environ['TABLE_ID'], job_config=job_config
        )  # Make an API request.
        load_job.result()  # Waits for the job to complete.
        
        print("success==",load_job.job_id,'===') 

        if (load_job.job_id and load_job.job_id!="") :
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(os.environ['PROJECT_ID'], os.environ['TOPIC_NAME'])

            message_json = json.dumps({
                'data': {'job_id': load_job.job_id, 'filename': data['name']},
            })
            message_bytes = message_json.encode('utf-8')
            # Publishes a message
            try:
                publish_future = publisher.publish(topic_path, data=message_bytes)
                publish_future.result()  # Verify the publish succeeded
                return 'Message published.'
            except Exception as e:
                print(e)
                return (e, 500)
    
