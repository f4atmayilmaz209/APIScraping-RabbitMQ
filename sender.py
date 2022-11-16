import pika, os, logging, time,json
logging.basicConfig()

url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello', durable=True)


with open("purple.json","r") as dd:
    for mes in dd.readlines():
        print(mes)
        channel.basic_publish(exchange='',
                            routing_key='hello',
                            body=json.dumps(mes),
                            properties=pika.BasicProperties(
                                delivery_mode = 2, # make message persistent
                            ))

        print(time.sleep(10))


# latest RabbitMQ 3.11
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management