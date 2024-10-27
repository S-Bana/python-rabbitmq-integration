import pika

def send_message_to_queue():
    """
    Sends messages to a RabbitMQ exchange using the Pika library.

    This function connects to a RabbitMQ server, declares an exchange of type 'direct',
    and publishes messages with different severity levels ('info', 'error', 'warning') 
    to the exchange. Each message is routed based on its severity key.

    Steps:
        1. Establishes a connection to RabbitMQ with provided credentials.
        2. Declares an exchange named 'logs' of type 'direct'.
        3. Publishes messages to the exchange with corresponding routing keys.

    Raises:
        pika.exceptions.AMQPConnectionError: If unable to connect to RabbitMQ server.
    """
    
    # Set up credentials for connecting to RabbitMQ
    credentials = pika.PlainCredentials(username='bob', password='bob')

    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', 
        port=5672,        
        credentials=credentials 
    ))

    # Create a channel for communication
    ch1 = connection.channel()

    # Declare an exchange of type 'direct'
    ch1.exchange_declare(exchange='logs', exchange_type='direct')

    # Define messages with their corresponding severity levels
    message_ = {
        'info': 'hello world',
        'error': 'error this message',
        'warning': 'warning this message'
    }

    # Publish each message to the exchange with its routing key
    for k, v in message_.items():
        ch1.basic_publish(
            exchange='logs', 
            routing_key=k,  
            body=v, 
        )

    print("Messages sent to the exchange.")

    # Close the connection
    connection.close()

# Execute the message sending function
send_message_to_queue()
