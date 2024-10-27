import pika


def send_message_to_queue():
    credentials = pika.PlainCredentials(username='bob', password='bob')

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', 
        port=5672,        
        credentials=credentials 
    ))

    ch1 = connection.channel()

    ch1.exchange_declare(exchange='logs', exchange_type='topic')

    message_ = {
        'info.debug.notimportant':'hello world',
        'error.warning.important':'error this message'
    }

    for k,v in message_.items():
        ch1.basic_publish(
            exchange='logs', 
            routing_key=k,  
            body=v, 
        )

    print("Message 'hello world' sent to all queues")

    connection.close()

send_message_to_queue()
