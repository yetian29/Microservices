from confluent_kafka import Consumer
import os, json, django
from rest_framework.exceptions import ValidationError


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()


consumer = Consumer({
    'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVER'),
    'security.protocol': 'SASL_SSL',
    'sasl.username': os.environ.get('KAFKA_USERNAME'), 
    'sasl.password': os.environ.get('KAFKA_PASSWORD'),
    'sasl.mechanism': 'PLAIN',
    'group.id': os.environ.get('KAFKA_GROUP'),
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([os.environ.get('KAFKA_TOPIC')])


try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError.PARTITION_EOF:
                print('Đã đọc hết partition')
            else:
                print(f'Lỗi: {msg.error()}')
        
        else:
            topic = msg.topic()
            value = msg.value()
            data = json.load(value)

            print(f"Got this message with Topic: {topic} and value: {value}, with Data: {data}")

            # if topic == os.environ.get('KAFKA_TOPIC'):
            #     if msg.key == b'create_user':
            #         try:
            #             print(f"Order created successfully for user {data['userID']}")
            #         except validationError as e:
            #             print(f"Failed to create order for user {data['userID']}: {str(e)}")
except KeyboardInterrupt:
    pass

finally:
    consumer.close()
