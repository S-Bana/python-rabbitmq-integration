"""
This script demonstrates how to set up a RabbitMQ consumer using the pika library.

It establishes a connection to a RabbitMQ server, declares a queue, and starts
consuming messages from that queue.
"""

import pika

# Set up credentials for RabbitMQ connection
credentials = pika.PlainCredentials(username='bob', password='bob')

# Establish a blocking connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=credentials
))

# Create a channel
ch1 = connection.channel()

# Declare a queue named 'que1'
ch1.queue_declare(queue='que1')

def call_back(ch, method, properties, body):
    """
    Callback function that is called when a message is received.

    Args:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): The method frame.
        properties (pika.spec.BasicProperties): Properties of the message.
        body (bytes): The message body.
    """
    print(f'Received {body}')

# Set up the consumer
ch1.basic_consume(
    queue='que1',
    on_message_callback=call_back,
    auto_ack=True  # Automatic acknowledgment of message receipt
)

# Start consuming messages
print('Waiting for messages. To exit press CTRL+C')
ch1.start_consuming()
