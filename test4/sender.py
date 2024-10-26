import pika

def send_message_to_queue():
    """
    Sends a message to a RabbitMQ exchange of type 'fanout'.

    This function establishes a connection to a RabbitMQ server using 
    the specified credentials, declares an exchange named 'logs', and 
    publishes a message ('hello world') to that exchange. The 'fanout' 
    exchange type broadcasts the message to all queues that are bound to it.

    The connection is closed after the message is sent.

    Raises:
        pika.exceptions.AMQPConnectionError: If the connection to RabbitMQ fails.
        pika.exceptions.ChannelError: If there is an error with the channel.
    """
    
    # Create credentials for connecting to RabbitMQ
    credentials = pika.PlainCredentials(username='bob', password='bob')

    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',  # RabbitMQ server hostname
        port=5672,        # Default port for RabbitMQ
        credentials=credentials  # User credentials
    ))

    # Create a channel for communication
    ch1 = connection.channel()

    # Declare an exchange of type 'fanout'
    ch1.exchange_declare(exchange='logs', exchange_type='fanout')

    # Publish a message to the 'logs' exchange
    ch1.basic_publish(
        exchange='logs',  # Target exchange
        routing_key='',   # Routing key (not used for fanout)
        body='hello world',  # Message body
    )

    print("Message 'hello world' sent to all queues")

    # Close the connection to RabbitMQ
    connection.close()

# Call the function to send the message
send_message_to_queue()
