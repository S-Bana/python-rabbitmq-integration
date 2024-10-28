import pika
import uuid


class Sender:
    def __init__(self):
        credentials = pika.PlainCredentials(username='bob', password='bob')

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            port=5672,        
            credentials=credentials 
        ))

        self.ch1 = self.connection.channel()
        result = self.ch1.queue_declare(queue='', exclusive=True)
        self.qname = result.method.queue
        self.ch1.basic_consume(
            queue=self.qname,
            on_message_callback=self.on_response,
            auto_ack=True
        )
    
    def on_response(self, ch, method, propertie, body):
        if self.corr_id == propertie.correlation_id:
            self.response = body
    
    def call_(self, num_in=0):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        send.ch1.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.qname,
                correlation_id=self.corr_id),
            body=str(num_in)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


send = Sender()
print(send.call_(30))
