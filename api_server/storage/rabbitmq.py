import json
import os
import time

import pika
import configparser
from loguru import logger as log


class Mq:
    """
    rabbitmq快速上手
    **************************
    数据流
    **************************
                                       /-->[队列(queue)]-->消费者
    生产者-->[交换机(exchange)](可选)———— --->[队列(queue)]-->消费者
                                       \-->[队列(queue)]-->消费者
    |||||||||||||||||||||||||||
    使用流程
    0、修改配置文件Rabbit.ini
    1、声明交换机(可选)、队列(declare_queue/exchange)
    2、将队列绑定至交换机(bind_queue)(无交换机即跳过)
    3、生产者投入数据(insert_message_into_exchange/queue)
    4、消费者使用数据(get_message)
    """
    def __init__(self):
        self.method_frame = None
        self.config = configparser.RawConfigParser()
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        self.config.read(os.path.join(parent_dir,'conf/Rabbit.ini'))
        self.connection = self.create_connection()
        self.channel = self.create_channel()

    def create_connection(self):
        """
        创建与RabbitMQ服务的连接
        :return: 连接对象
        """
        error_count = 0
        while error_count < int(self.config.get('server', 'connection_error_count')):
            try:
                credentials = pika.PlainCredentials(username=self.config.get('server', 'username'),
                                                    password=self.config.get('server', 'password'))
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.config.get('server', 'host'),
                                              port=self.config.getint('server', 'port'),
                                              credentials=credentials))
                return connection
            except Exception as e:
                error_count += 1
                log.warning(f'创建与RabbitMQ服务的连接失败,{e},进行第{error_count}次重试')
                time.sleep(1)
        log.critical('创建与RabbitMQ服务的连接失败,重试次数达到上限')
        raise 'RabbitMq:connection Error'

    def create_channel(self):
        """
        创建通道
        :return: 通道
        """
        error_count = 0
        while error_count < int(self.config.get('server', 'channel_error_count')):
            try:
                channel = self.connection.channel()
                return channel
            except Exception as e:
                error_count += 1
                log.warning(f'创建通道失败,{e},进行第{error_count}次重试')
                time.sleep(1)
        log.critical('创建通道失败,重试次数达到上限')
        raise 'RabbitMq:channel Error'

    def check_connection(self):
        try:
            if not self.connection.is_open:
                self.connection = self.create_connection()
        except:
            self.connection = self.create_connection()

    def check_channel(self):
        try:
            self.check_connection()
            if not self.channel.is_open:
                self.channel = self.create_channel()
        except:
            self.channel = self.create_channel()

    def init_queue(self,queue_list):
        for queue in queue_list:
            self.channel.queue_delete(queue)
            self.declare_queue(queue)

    def clean_queue(self, queue_name):
        """
        清空队列
        :return:
        """
        data = self.get_message(queue_name)
        while data:
            data = self.get_message(queue_name)

    def declare_queue(self, queue_name, durable=True, exclusive=False):
        """
        声明队列
        :param queue_name: str,队列名称
        :param durable: bool,是否持久化
        :param exclusive: boot,是否私有化
        :return:
        """
        try:
            self.check_channel()
            self.channel.queue_declare(queue_name, durable=durable, exclusive=exclusive)
        except Exception as e:
            log.error('declare_queue:' + queue_name + str(e))
            raise e

    def declare_exchange(self, exchange_name, exchange_type='fanout', durable=True):
        """
        声明交换机
        :param exchange_name: str,交换机名称
        :param durable: bool,是否持久化
        :return:
        """
        try:
            self.check_channel()
            self.channel.exchange_declare(exchange=exchange_name, durable=durable,exchange_type=exchange_type)
        except Exception as e:
            log.error('declare_exchange:' + exchange_name + str(e))
            raise e

    def bind_queue(self, queue_name, exchange):
        """
        将队列绑定到交换机上
        :param queue_name: str, 队列名称
        :param exchange: str, 交换机名称
        :return:
        """
        try:
            self.check_channel()
            self.channel.queue_bind(queue_name, exchange)
        except Exception as e:
            log.error('bind_queue:'+queue_name+'to'+exchange+str(e))

    def insert_message_into_exchange(self, exchange_name, data, exchange_type='fanout', routing_key=''):
        """
        将消息投入交换机
        :param routing_key: str
        :param exchange_type: Str,交换机类型，非fanout类型需要指定routing_key
        :param exchange_name: Str,交换机名称
        :param data: Any, 数据
        :return:
        """
        try:
            if exchange_type != 'fanout' and routing_key == '':
                raise 'MUST SET ROUTING_KEY'
            body = {'insert_time': time.strftime(self.config.get('insert', 'time_format'), time.localtime()),
                    'data': data}
            body_json = json.dumps(body, ensure_ascii=False)
            body_byte = body_json.encode()
            self.channel.basic_publish(exchange=exchange_name,
                                       routing_key=routing_key,
                                       body=body_byte,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,  # make message persistent
                                       )
                                       )
        except Exception as e:
            log.error('insert_message_into_exchange:' + exchange_name + str(e))

    def insert_message_into_queue(self, queue_name, data):
        """
        向消息队列中插入消息
        :param queue_name: str,队列名称
        :param data: Any,消息数据
        :return: 'ok'
        """
        try:
            self.check_channel()
            self.declare_queue(queue_name)
            body = {'insert_time': time.strftime(self.config.get('insert', 'time_format'), time.localtime()),
                    'data': data}
            body_json = json.dumps(body, ensure_ascii=False)
            body_byte = body_json.encode()
            self.channel.basic_publish(exchange='',
                                       routing_key=queue_name,
                                       body=body_byte,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,  # make message persistent
                                       )
                                       )
        except Exception as e:
            log.error(f'insert_message_into_queue:{queue_name}{e}')
            raise e

    def get_message_not_ack(self, queue_name):
        """
        获取消息，不自动确认，确认即调用ack_this_message，不确认即调用close_channel
        :param queue_name: str,队列名称
        :return:
        """
        try:
            self.check_channel()
            self.channel.basic_qos(prefetch_count=1)
            self.method_frame, header_frame, data = self.channel.basic_get(queue_name)
            # 若队列为空，则返回空
            if not data:
                return data
            data = data.decode()
            data = json.loads(data)
            data['get_time'] = time.strftime(self.config.get('get', 'time_format'))
            return data
        except Exception as e:
            log.error('get_message_not_ack:'+queue_name+str(e))
            raise e

    def ack_this_message(self):
        self.check_channel()
        self.channel.basic_ack(self.method_frame.delivery_tag)

    def get_message(self, queue_name):
        """
        从消息队列获取消息
        :param queue_name: str,队列名称
        :return: dict,消息 or 'timeout'
        """
        try:
            self.check_channel()
            self.channel.basic_qos(prefetch_count=1)
            method_frame, header_frame, data = self.channel.basic_get(queue_name)
            # 若队列为空，则返回空
            if not data:
                return data
            data = data.decode()
            self.channel.basic_ack(method_frame.delivery_tag)
            raw = json.loads(data)
            raw['get_time'] = time.strftime(self.config.get('get', 'time_format'))
            return raw
        except Exception as e:
            log.error('get_message:'+queue_name+str(e))
            raise e

    def get_message_count(self, queue_name):
        """
        获取队列消息数
        :param queue_name: str,队列名称
        :return: int, 消息数量
        """
        try:
            self.check_channel()
            queue = self.channel.queue_declare(queue=queue_name, passive=True)
            return queue.method.message_count
        except Exception as e:
            log.error('get_message_count:'+queue_name+str(e))
            raise e

    def close_connection(self):
        """
        关闭连接
        :return:
        """
        self.connection.close()

    def close_channel(self):
        """
        关闭通道
        :return:
        """
        self.channel.close()

    def close_all(self):
        """
        关闭通道与连接
        :return:
        """
        self.close_channel()
        self.create_connection()

rabbit = Mq()
if __name__ == '__main__':
    rabbit = Mq()
    print('test')
