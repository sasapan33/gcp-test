import firebase_admin
from firebase_admin import messaging
import os
from firebase_admin import credentials

cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
default_app = firebase_admin.initialize_app()

topic = 'highScores'
message = messaging.Message(
    data={
        'score': '850',
        'time': '2:45',
    },
    topic=topic,
)

response = messaging.send(message)

print('success', response)
