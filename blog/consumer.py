from confluent_kafka import Consumer
import os, json, django
from rest_framework.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

consumer =  Consumer({
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
        msg = consumer.poll(1.0) # lay du lieu trong 1s

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError.PARTITION_EOF: #Điều này kiểm tra xem lỗi trả về có phải là lỗi "Kết thúc của Partition" hay không. Khi một consumer đã đọc hết dữ liệu trong một partition, Kafka sẽ trả về lỗi PARTITION_EOF. Điều này giúp consumer biết khi nào nên dừng việc đọc trong trường hợp không có dữ liệu mới.
                  print('Đã đọc hết partition')
            else:
                print(f'Lỗi: {msg.error()}')
        else:
            topic = msg.topic()
            value = msg.value()
            data = json.load(value)

            print(f"Got this message with topic: {topic} and value: {value}, with Data: {data}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
            

