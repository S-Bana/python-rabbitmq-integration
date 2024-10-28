# import pika


# class Sender:
#     def __init__(self):
#         credentials = pika.PlainCredentials(username='bob', password='bob')

#         connection = pika.BlockingConnection(pika.ConnectionParameters(
#             host='localhost', 
#             port=5672,        
#             credentials=credentials 
#         ))

#         self.ch1 = connection.channel()
#         result = self.ch1.queue_declare(queue='rpc_queue', exclusive=True)
#         self.qname = result.method.queue
    
#     def call_back(self, ch, method, propertie, body):
#         print(f'Received: {body.decode()}')
#         n = int(body)
#         response = n + 1
#         self.ch1.basic_publish(
#             exchange='',
#             routing_key=propertie.reply_to,
#             properties=pika.BasicProperties(correlation_id=propertie.correlation_id),
#             body=str(response)
#         )
#         self.ch1.basic_ack(delivery_tag=method.delivery_tag)
#         print(f'Send: {response}')

#     def call_(self):
#         self.ch1.basic_qos(prefetch_count=1)
#         self.ch1.basic_consume(queue='rpc_queue', on_message_callback=self.call_back)
#         print('Waiting for messages. To exit press CTRL+C')
#         self.ch1.start_consuming()


# s = Sender()
# s.call_()


import pika

class Receiver:
    """
    A class to represent a RabbitMQ message receiver.

    This class establishes a connection to a RabbitMQ server, declares a queue,
    and listens for incoming messages. When a message is received, it processes
    the message and sends back a response.
    """

    def __init__(self):
        """
        Initializes the Receiver instance by establishing a connection to the RabbitMQ server
        and declaring an exclusive queue named 'rpc_queue'.

        Attributes:
            ch1 (pika.Channel): The channel used for communication with RabbitMQ.
            qname (str): The name of the declared queue.
        """
        # Set up credentials for RabbitMQ
        credentials = pika.PlainCredentials(username='bob', password='bob')

        # Establish a connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            port=5672,        
            credentials=credentials 
        ))

        # Create a channel
        self.ch1 = connection.channel()
        
        # Declare an exclusive queue for RPC communication
        result = self.ch1.queue_declare(queue='rpc_queue', exclusive=True)
        self.qname = result.method.queue

    def call_back(self, ch, method, properties, body):
        """
        Callback function that is called when a message is received from the queue.

        This function processes the incoming message by converting it to an integer,
        increments it by one, and sends the response back to the specified reply-to queue.

        Args:
            ch (pika.Channel): The channel object used for communication.
            method (pika.Basic.Deliver): Delivery information for the message.
            properties (pika.BasicProperties): Properties associated with the message.
            body (bytes): The body of the received message.
        """
        print(f'Received: {body.decode()}')
        
        # Convert the received message to an integer and increment it
        n = int(body)
        response = n + 1
        
        # Publish the response back to the reply-to queue
        self.ch1.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(response)
        )
        
        # Acknowledge that the message has been processed
        self.ch1.basic_ack(delivery_tag=method.delivery_tag)
        
        print(f'Sent: {response}')

    def call_(self):
        """
        Starts consuming messages from the 'rpc_queue'.

        This method sets up Quality of Service (QoS) settings to ensure that only one 
        message is sent at a time to this consumer. It then waits for messages 
        and processes them using the call_back method.
        
        To exit this method, press CTRL+C in the console.
        """
        # Set QoS settings
        self.ch1.basic_qos(prefetch_count=1)
        
        # Start consuming messages from the queue
        self.ch1.basic_consume(queue='rpc_queue', on_message_callback=self.call_back)
        
        print('Waiting for messages. To exit press CTRL+C')
        
        # Start consuming messages
        self.ch1.start_consuming()

# Create an instance of Receiver and start listening for messages
s = Receiver()
s.call_()
