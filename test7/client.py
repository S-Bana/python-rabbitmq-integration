# import pika
# import uuid


# class Sender:
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
#         self.ch1.basic_consume(
#             queue=self.qname,
#             on_message_callback=self.on_response,
#             auto_ack=True
#         )
    
#     def on_response(self, ch, method, propertie, body):
#         if self.corr_id == propertie.correlation_id:
#             self.response = body
    
#     def call_(self, num_in=0):
#         self.response = None
#         self.corr_id = str(uuid.uuid4())
#         send.ch1.basic_publish(
#             exchange='',
#             routing_key='rpc_queue',
#             properties=pika.BasicProperties(
#                 reply_to=self.qname,
#                 correlation_id=self.corr_id),
#             body=str(num_in)
#         )
#         while self.response is None:
#             self.connection.process_data_events()
#         return int(self.response)


# send = Sender()
# print(send.call_(30))


import pika
import uuid

class Sender:
    """
    A class to represent a RabbitMQ RPC client.

    This class establishes a connection to a RabbitMQ server, declares an exclusive
    queue for receiving responses, and provides a method to send messages to a specified
    queue and wait for responses.
    """

    def __init__(self):
        """
        Initializes the Sender instance by establishing a connection to the RabbitMQ server,
        declaring an exclusive response queue, and setting up the consumer for that queue.

        Attributes:
            connection (pika.BlockingConnection): The connection to the RabbitMQ server.
            ch1 (pika.Channel): The channel used for communication with RabbitMQ.
            qname (str): The name of the declared exclusive response queue.
        """
        # Set up credentials for RabbitMQ
        credentials = pika.PlainCredentials(username='bob', password='bob')

        # Establish a connection to the RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            port=5672,        
            credentials=credentials 
        ))

        # Create a channel
        self.ch1 = self.connection.channel()
        
        # Declare an exclusive queue for receiving responses
        result = self.ch1.queue_declare(queue='', exclusive=True)
        self.qname = result.method.queue
        
        # Set up the consumer to listen for responses on the exclusive queue
        self.ch1.basic_consume(
            queue=self.qname,
            on_message_callback=self.on_response,
            auto_ack=True  # Automatically acknowledge messages
        )

    def on_response(self, ch, method, properties, body):
        """
        Callback function that is called when a response message is received.

        This function checks if the correlation ID of the received message matches
        the correlation ID of the sent message. If they match, it stores the response.

        Args:
            ch (pika.Channel): The channel object used for communication.
            method (pika.Basic.Deliver): Delivery information for the message.
            properties (pika.BasicProperties): Properties associated with the message.
            body (bytes): The body of the received message.
        """
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call_(self, num_in=0):
        """
        Sends a request to the RPC server and waits for a response.

        This method generates a unique correlation ID, sends a message containing
        the input number, and waits until a matching response is received.

        Args:
            num_in (int): The input number to send in the RPC request. Default is 0.

        Returns:
            int: The integer value from the response body after conversion.
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())  # Generate a unique correlation ID
        
        # Publish the request message to the 'rpc_queue'
        self.ch1.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.qname,
                correlation_id=self.corr_id),
            body=str(num_in)
        )
        
        # Wait for a response
        while self.response is None:
            self.connection.process_data_events()
        
        return int(self.response)  # Convert response body to integer


# Create an instance of Sender and send a request
send = Sender()
print(send.call_(30))  # Example call with input number 30
