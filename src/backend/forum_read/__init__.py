import signal
from .consumer import Consumer


def cancel(*args, **kwargs):
    from .consumer import Consumer
    Consumer.instance.cancel()


consumer = Consumer()
consumer.start_consuming()
signal.signal(signal.SIGINT, cancel)
