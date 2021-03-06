__author__ = 'gx'
import mongoengine
import datetime
import hashlib
from smm import config
from smm.classifier import labels

class StreamSource(object):
    TWITTER = "twitter"


class RawStreamQueue(mongoengine.Document):
    text = mongoengine.StringField(required=True, max_length=1024)
    source = mongoengine.StringField(required=True)
    original = mongoengine.DictField()


class ClassifiedStream(mongoengine.Document):
    meta = {
        'indexes': ['tokens'],
    }

    text = mongoengine.StringField(required=True, max_length=1024)
    polarity = mongoengine.FloatField()
    tokens = mongoengine.ListField(mongoengine.StringField(max_length=64))
    source = mongoengine.StringField(required=True)
    original = mongoengine.DictField()


class SocketSession(mongoengine.Document):
    meta = {
        'indexes': ['ip', 'ttl'],
    }

    TTL = 30
    ip = mongoengine.StringField(required=True, max_length=45)
    keywords = mongoengine.ListField(mongoengine.StringField(max_length=64))
    ttl = mongoengine.DateTimeField(default=datetime.datetime.now)

    def ping(self):
        self.ttl = datetime.datetime.now()
        self.save()

    @classmethod
    def remove_expired(cls):
        d = datetime.datetime.now() - datetime.timedelta(seconds=cls.TTL)
        cls.objects(ttl__lte=d).delete()

    @classmethod
    def get_keywords(cls):
        cls.remove_expired()
        k = set()
        for s in cls.objects:
            k.update(set(s.keywords))

        return k

    @classmethod
    def get_keywords_hash(cls):
        k = str(cls.get_keywords())
        return hashlib.sha1(k).hexdigest()


class TrainDataRaw(mongoengine.Document):
    text = mongoengine.StringField(required=True, max_length=1024)
    polarity = mongoengine.FloatField()
    original = mongoengine.DictField()

    meta = {
        'indexes': ['polarity'],
    }

    def get_label(self):
        if self.polarity == -1:
            return labels.negative
        else:
            return labels.positive


class TrainedClassifiers(mongoengine.Document):
    name = mongoengine.StringField(required=True, max_length=256, unique=True)
    classifier = mongoengine.BinaryField()
    stats = mongoengine.DictField()


def connect(conf=config.mongo_db):
    mongoengine.connect(**conf)