'''
docker run -d
    --hostname my-rabbit
    --name some-rabbit
    -e RABBITMQ_DEFAULT_USER=bob
    -e RABBITMQ_DEFAULT_PASS=bob
    -p 5672:5672
    -p 15672:15672
    rabbitmq:3-management
'''

import pika


def call_back(ch, method, properties, body):
    """
    Callback function that is called when a message is received from the queue and process incoming messages.

    Args:
        ch: The channel object that received the message.
        method: The method frame containing delivery information.
        properties: The properties of the message.
        body: The content of the message received.

    This function prints the received message and acknowledges its receipt.
    """
    print(f'Received header: {properties.headers} - message: {body}')
    # Acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages_from_queue():
    """
    Connects to a RabbitMQ server and consumes messages from a specified queue.

    This function performs the following steps:
    1. Creates credentials for connecting to RabbitMQ using a username and password.
    2. Establishes a blocking connection to the RabbitMQ server running on localhost.
    3. Declares a queue named 'que1', ensuring it is durable and passive.
    4. Configures Quality of Service (QoS) settings to limit the number of unacknowledged messages.
    5. Starts consuming messages from the declared queue.

    Note:
        Ensure that RabbitMQ is running on the specified host and port before executing this function.
    """
    
    # Create credentials for RabbitMQ connection
    credentials = pika.PlainCredentials(username='bob', password='bob')

    # Establish a blocking connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    ))

    # Create a channel for communication
    ch1 = connection.channel()

    # Declare a queue named 'que1'
    # If the queue doesn't exist, it will be created
    ch1.queue_declare(queue='que1')

    # Declare a durable and passive queue named 'que1'
    ch1.queue_declare(
        queue='que1',
        durable=True,
        passive=True
    )

    # Set QoS settings to limit the number of unacknowledged messages
    ch1.basic_qos(prefetch_count=1)

    # Start consuming messages from the declared queue with the specified callback
    ch1.basic_consume(
        queue='que1',
        on_message_callback=call_back,
    )

    print('Waiting for messages. To exit press CTRL+C')
    
    # Start consuming messages indefinitely
    ch1.start_consuming()

# Call the function to start consuming messages
consume_messages_from_queue()