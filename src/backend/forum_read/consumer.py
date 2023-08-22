import json
import threading

import pika


def callback(ch, method, properties, body):
    from .models import ThreadCategory, Thread, ThreadVote, TaggedThread
    content_type = properties.content_type
    data = json.loads(body)
    print("Received reader: ", content_type, data)
    # Category
    if content_type == 'thread_category_saved':
        category, create = ThreadCategory.objects.update_or_create(name=data['name'], defaults=data)
        print("Category created", create)
    elif content_type == 'thread_category_deleted':
        category = ThreadCategory.objects.get(name=data['name'])
        if category is not None:
            category.delete()
            print("Category deleted")
    # Thread
    elif content_type == 'thread_saved':
        th, create = Thread.objects.update_or_create(id=data['id'], defaults=data)
        print("Thread created", create)
    elif content_type == 'thread_deleted':
        th = Thread.objects.get(id=data['id'])
        if th is not None:
            th.delete()
            print("Thread deleted")
    # Thread votes
    elif content_type == 'thread_vote_saved':
        vote, create = ThreadVote.objects.update_or_create(thread=data['thread'],
                                                           user_id=data['user_id'],
                                                           defaults=data)
        print("Thread vote created", vote)
    elif content_type == 'thread_vote_deleted':
        vote = ThreadVote.objects.get(thread=data['thread'], user_id=data['user_id'])
        if vote is not None:
            vote.delete()
            print("Thread vote deleted")
    # Thread tags
    elif content_type == 'thread_tag_saved':
        tag, create = TaggedThread.objects.update_or_create(thread=data['thread'],
                                                            tag_id=data['tag_id'],
                                                            defaults=data)
        print("Thread tag created", create)
    elif content_type == 'thread_tag_deleted':
        tag = TaggedThread.objects.get(thread=data['thread'], tag_id=data['tag_id'])
        if tag is not None:
            tag.delete()
            print("Thread tag deleted")


class Consumer:

    instance = None

    def __init__(self):
        self.thread = None
        (self.conn, self.channel) = self.init_channel()
        Consumer.instance = self

    @staticmethod
    def init_channel():
        from django.conf import settings
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBIT_MQ_URL,
                                      credentials=pika.credentials.PlainCredentials('udptgroup1', 'udptgroup1'),
                                      heartbeat=600,
                                      blocked_connection_timeout=300))
        channel = conn.channel()
        channel.queue_declare(queue='forum')
        return conn, channel

    def start_consuming(self):
        self.channel.basic_consume(queue='forum', on_message_callback=callback, auto_ack=True)
        self.thread = threading.Thread(target=self.__start_consuming)
        self.thread.start()

    def __start_consuming(self):
        print("start consuming")
        self.channel.start_consuming()
        print("close")

    def cancel(self):
        print("cancel")
        self.channel.stop_consuming()
        self.conn.close()
        try:
            self.thread.join()
        except Exception:
            pass
