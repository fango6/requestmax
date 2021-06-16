import csv

from kafka import KafkaConsumer, KafkaProducer


class Csv(object):
    ''' csv 读写器, 读:DictReader, 写:DictWriter
    '''

    @staticmethod
    def reader(file_path, field_names, encoding="utf-8"):
        '''
        rgen = reader('./test.csv', ['column1', 'column2'])
        for item in rgen:
            print(item)
        '''
        with open(file_path, encoding=encoding) as fp:
            reader = csv.DictReader(fp, field_names)
            _headers = next(reader)
            for item in reader:
                yield item

    @staticmethod
    def writer(file_path, field_names, mode='w', encoding='utf-8'):
        '''
        wgen = writer('./test.csv', ['column1', 'column2'])
        wgen.send(None)
        wgen.send({'column1':'a', 'column2':'b'})
        '''
        with open(file_path, mode, encoding=encoding, newline='') as fp:
            writer = csv.DictWriter(fp, field_names)
            writer.writeheader()
            while True:
                recv = yield
                if not recv:
                    break
                writer.writerow(recv)


class Kafka(object):

    @staticmethod
    def consumer(addrs, topics, offset_reset="latest", group_id=None, **kwargs):
        consumer = KafkaConsumer(
            topics,
            bootstrap_servers=addrs,
            auto_offset_reset=offset_reset,
            group_id=group_id,
            **kwargs)
        for msg in consumer:
            yield msg.value

    @staticmethod
    def producer(addrs, **kwargs):
        producer = KafkaProducer(
            bootstrap_servers=addrs, **kwargs)
        while True:
            recv = yield
            if not recv:
                break
            producer.send(**recv)
