import pika

credentials = pika.PlainCredentials(username='bob', password='bob')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

ch1 = connection.channel()

ch1.queue_declare(queue='que1')

def call_back(ch, method, properties, body):
    print(f'Recived {body}')

ch1.basic_consume(queue='que1',
                  on_message_callback=call_back,
                  auto_ack=True)

ch1.start_consuming()