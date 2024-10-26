import pika

def send_message_to_queue():
    """
    Establishes a connection to a RabbitMQ server and sends a message to a specified queue.

    This function performs the following steps:
    1. Creates credentials for connecting to RabbitMQ using a username and password.
    2. Establishes a blocking connection to the RabbitMQ server running on localhost.
    3. Declares a queue named 'que1', ensuring it is durable and passive.
    4. Publishes a message ('hello world') to the declared queue with delivery mode set to persistent.
    5. Closes the connection after sending the message.

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

    # Declare a durable and passive queue named 'que1'
    ch1.queue_declare(
        queue='que1',
        durable=True,
        passive=True
    )

    # Publish a message to the declared queue with persistent delivery mode
    ch1.basic_publish(
        exchange='',  
        routing_key='que1', 
        body='hello world', 
        properties=pika.BasicProperties(delivery_mode=2,)
    )

    print("Message 'hello world' sent to queue 'que1'")

    # Close the connection to the RabbitMQ server
    connection.close()

# Call the function to send the message
send_message_to_queue()
