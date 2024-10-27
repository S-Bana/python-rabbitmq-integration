import pika

def call_back(ch, method, properties, body):
    print(f'Received message: {body}')

def consume_messages_from_queue():

    credentials = pika.PlainCredentials(username='bob', password='bob')

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', 
        port=5672,
        credentials=credentials
    ))

    ch1 = connection.channel()

    ch1.exchange_declare(exchange='logs2', exchange_type='topic')

    result = ch1.queue_declare(queue='', exclusive=True)
    
    qname = result.method.queue

    binding_key = '#.notimportant'

    ch1.queue_bind(exchange='logs2', queue=qname, routing_key=binding_key)

    print('Waiting for messages. To exit press CTRL+C')
    
    ch1.basic_consume(queue=qname, on_message_callback=call_back, auto_ack=True)

    ch1.start_consuming()

consume_messages_from_queue()
