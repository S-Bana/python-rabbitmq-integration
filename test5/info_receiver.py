import pika

def call_back(ch, method, properties, body):
    print(f'Received method: {method.routing_key} \t message: {body}')


def consume_messages_from_queue():
   
    credentials = pika.PlainCredentials(username='bob', password='bob')

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', 
        port=5672,
        credentials=credentials
    ))

    ch1 = connection.channel()

    ch1.exchange_declare(exchange='logs', exchange_type='fanout')

    result = ch1.queue_declare(
                queue='', 
                exclusive=True 
            )
    
    qname = result.method.queue

    severities = ('info', 'error', 'warning')

    for sev in severities:
        ch1.queue_bind(exchange='logs', queue=qname, routing_key=sev)

    print('Waiting for messages. To exit press CTRL+C')
    
    ch1.basic_consume(queue=qname, on_message_callback=call_back, auto_ack=True)

    ch1.start_consuming()

consume_messages_from_queue()
