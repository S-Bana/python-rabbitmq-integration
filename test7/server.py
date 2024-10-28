import pika


class Sender:
    def __init__(self):
        credentials = pika.PlainCredentials(username='bob', password='bob')

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            port=5672,        
            credentials=credentials 
        ))

        self.ch1 = connection.channel()
        result = self.ch1.queue_declare(queue='rpc_queue', exclusive=True)
        self.qname = result.method.queue
    
    def call_back(self, ch, method, propertie, body):
        print(f'Received: {body.decode()}')
        n = int(body)
        response = n + 1
        self.ch1.basic_publish(
            exchange='',
            routing_key=propertie.reply_to,
            properties=pika.BasicProperties(correlation_id=propertie.correlation_id),
            body=str(response)
        )
        self.ch1.basic_ack(delivery_tag=method.delivery_tag)
        print(f'Send: {response}')

    def call_(self):
        self.ch1.basic_qos(prefetch_count=1)
        self.ch1.basic_consume(queue='rpc_queue', on_message_callback=self.call_back)
        print('Waiting for messages. To exit press CTRL+C')
        self.ch1.start_consuming()


s = Sender()
s.call_()
