
import pika

credentials = pika.PlainCredentials(username='bob', password='bob')

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=credentials
))

ch1 = connection.channel()

ch1.queue_declare(
    queue='que1',
    durable=True,
    passive=True
    )

def call_back(ch, method, properties, body):
    print(f'Received {body}')
    ch1.basic_ack(delivery_tag=method.delivery_tag)

ch1.basic_qos(prefetch_count=1)
ch1.basic_consume(
    queue='que1',
    on_message_callback=call_back,
)

print('Waiting for messages. To exit press CTRL+C')
ch1.start_consuming()
