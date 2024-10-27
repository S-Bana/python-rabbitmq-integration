# import pika

# class Receiver:
#     def __init__(self):
#         credentials = pika.PlainCredentials(username='bob', password='bob')

#         self.connection = pika.BlockingConnection(pika.ConnectionParameters(
#             host='localhost', 
#             port=5672,        
#             credentials=credentials 
#         ))

#         self.ch1 = self.connection.channel()
#         result = self.ch1.queue_declare(queue='', exclusive=True)
#         self.qname = result.method.queue
    
#     def call_back(self, ch, method, propertie, body):
#         print(f'Received: {body}')
#         n = int(body)
#         response = n + 1
#         self.ch1.basic_publish(
#             exchange='',
#             routing_key=propertie.reply_to,
#             properties=pika.BasicProperties(correlation_id=propertie.correlation_id),
#             body=str(response)
#         )
#         self.ch1.basic_ack(delivery_tag=method.delivery_tag)


#     def call_(self):
#         self.ch1.basic_qos(prefetch_count=1)
#         self.ch1.basic_consume(queue=self.qname, on_message_callback=self.call_back)
#         print('Waiting for messages. To exit press CTRL+C')
#         self.ch1.start_consuming()


# send = Receiver()
# send.call_()

import pika
import sys

class Receiver:
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
        
        # Set QoS settings
        self.ch1.basic_qos(prefetch_count=1)

    def call_back(self, ch, method, properties, body):
        print(f'Received: {body}')
        try:
            n = int(body)
            response = n + 1
            
            # Publish response back to the requester
            self.ch1.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=str(response)
            )
            # Acknowledge the message
            self.ch1.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            # Optionally, you could reject the message or handle it differently
            self.ch1.basic_nack(delivery_tag=method.delivery_tag)

    def call_(self):
        self.ch1.basic_consume(queue=self.qname, on_message_callback=self.call_back)
        print('Waiting for messages. To exit press CTRL+C')
        
        try:
            self.ch1.start_consuming()
        except KeyboardInterrupt:
            print('Shutting down...')
            self.close()

    def close(self):
        if self.connection:
            self.connection.close()

# Usage example
if __name__ == "__main__":
    receiver = Receiver()
    receiver.call_()
