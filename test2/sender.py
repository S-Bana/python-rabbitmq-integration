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

ch1.basic_publish(
    exchange='',  
    routing_key='que1', 
    body='hello world', 
    properties=pika.BasicProperties(delivery_mode=2,)
)

print("Message 'hello world' sent to queue 'que1'")

connection.close()
