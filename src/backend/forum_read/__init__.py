import signal


def cancel():
    from .consumer import Consumer
    Consumer.instance.cancel()


signal.signal(signal.SIGINT, cancel)
