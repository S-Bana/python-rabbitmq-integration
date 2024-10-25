import pika

credentials = pika.PlainCredentials(username='bob', password='bob')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

ch1 = connection.channel()

ch1.queue_declare(queue='que1')

ch1.basic_publish(exchange='',
                  routing_key='que1',
                  body='hello world')

connection.close()
