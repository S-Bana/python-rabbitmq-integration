import pika

def call_back(ch, method, properties, body):
    """
    Callback function that is called when a message is received.

    Args:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Delivery method information.
        properties (pika.spec.Basic.Properties): Message properties.
        body (bytes): The message body that was received.
    """
    print(f'Received message: {body.decode()}')  # Decode bytes to string for display


def consume_messages_from_queue():
    """
    Consumes messages from a RabbitMQ exchange of type 'fanout'.

    This function establishes a connection to a RabbitMQ server using 
    the specified credentials, declares an exchange named 'logs', 
    creates a temporary exclusive queue, binds it to the exchange, 
    and starts consuming messages from that queue. The messages are 
    processed by the `call_back` function.

    Raises:
        pika.exceptions.AMQPConnectionError: If the connection to RabbitMQ fails.
        pika.exceptions.ChannelError: If there is an error with the channel.
        pika.exceptions.ChannelClosed: If the channel is closed unexpectedly.
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

    # Declare an exclusive temporary queue
    result = ch1.queue_declare(
                queue='',  # Use an empty string for a unique queue name
                exclusive=True  # Queue will be deleted when the connection closes
            )
    
    qname = result.method.queue  # Get the name of the temporary queue

    # Bind the temporary queue to the 'logs' exchange
    ch1.queue_bind(exchange='logs', queue=qname)

    print('Waiting for messages. To exit press CTRL+C')
    
    # Start consuming messages from the bound queue
    ch1.basic_consume(queue=qname, on_message_callback=call_back, auto_ack=True)

    # Start processing incoming messages
    ch1.start_consuming()

# Call the function to start consuming messages
consume_messages_from_queue()
