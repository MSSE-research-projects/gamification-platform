# Define a singleton class to act as a mediator between the views and the models.
# This class is responsible for passing data between the views and the models.


def register_subscriber():
    def _wrapper(cls):
        mediator = Publisher()
        mediator.add_subscriber(cls(mediator))
    return _wrapper


class Publisher:

    subscribers = []

    def __new__(cls):
        '''
        Singleton class
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(Publisher, cls).__new__(cls)
        return cls.instance

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, receiver, message, obj=None):
        '''
        If obj is None, the receiver should handle the logic of
        creating/updating/deleting the object.
        '''
        for r in self.subscribers:
            if r.__class__ == receiver:
                r.handle(message, obj)


class Subscriber:

    def __init__(self, publisher: Publisher):
        self.publisher = publisher

    def handle(self, message, obj, *args, **kwargs):
        func = getattr(self, message)
        if func:
            func(obj, *args, **kwargs)
        else:
            raise ValueError('Invalid message')

    def create(self, obj, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement 'create' method")

    def update(self, obj, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement 'update' method")

    def delete(self, obj, commit=True):
        raise NotImplementedError("Subclasses must implement 'delete' method")
