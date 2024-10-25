"""
This script demonstrates how to publish a message to a RabbitMQ queue using the pika library.

It establishes a connection to a RabbitMQ server, declares a queue, publishes a message to that queue,
and then closes the connection.
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
# If the queue doesn't exist, it will be created
ch1.queue_declare(queue='que1')

# Publish a message to the queue
ch1.basic_publish(
    exchange='',  # Use the default exchange
    routing_key='que1',  # The queue to publish to
    body='hello world'  # The message body
)

print("Message 'hello world' sent to queue 'que1'")

# Close the connection
connection.close()
