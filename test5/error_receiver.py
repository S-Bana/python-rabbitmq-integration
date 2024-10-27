import pika

def call_back(ch, method, properties, body):
    """
    Callback function to handle incoming error messages from the queue.

    Args:
        ch (pika.channel.Channel): The channel object used to communicate with RabbitMQ.
        method (pika.spec.Basic.Deliver): Contains delivery information, including the routing key.
        properties (pika.spec.BasicProperties): Contains message properties such as headers.
        body (bytes): The message body received from the queue.
        
    Logs:
        Appends the received message body to 'error_logs.log' file.
    """
    # Log the received message to a file
    with open('error_logs.log', 'a') as log_:
        log_.write(body.decode() + '\n')  # Decode bytes to string before writing

def consume_messages_from_queue():
    """
    Consumes error messages from a RabbitMQ queue using the Pika library.

    This function connects to a RabbitMQ server, declares an exchange,
    creates a temporary exclusive queue, binds it to the exchange for 
    error messages, and starts consuming messages. Incoming messages are 
    logged to 'error_logs.log'.

    Steps:
        1. Establishes a connection to RabbitMQ with provided credentials.
        2. Declares an exchange named 'logs' of type 'direct'.
        3. Creates an exclusive temporary queue for receiving error messages.
        4. Binds the queue to the exchange for the 'error' routing key.
        5. Waits for messages and processes them using the callback function.

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

    # Declare an exclusive temporary queue
    result = ch1.queue_declare(queue='', exclusive=True)
    
    # Get the name of the created queue
    qname = result.method.queue

    # Bind the queue to the exchange for 'error' severity messages
    severities = 'error'
    ch1.queue_bind(exchange='logs', queue=qname, routing_key=severities)

    print('Waiting for error messages. To exit press CTRL+C')
    
    # Start consuming messages from the queue with a callback function
    ch1.basic_consume(queue=qname, on_message_callback=call_back, auto_ack=True)

    # Begin consuming messages
    ch1.start_consuming()

# Execute the message consumption function
consume_messages_from_queue()
