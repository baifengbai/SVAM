import configparser
import os
import re

import pymysql
from loguru import logger as log

class SqlAction():
    def __init__(self):
        self.config = configparser.RawConfigParser()
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        self.config.read(os.path.join(parent_dir,'conf/Mysql.ini'))
        host = self.config.get('common','host')
        port = int(self.config.get('common','port'))
        user = self.config.get('common', 'user')
        password = self.config.get('common', 'password')
        database = self.config.get('common', 'database')
        try:
            self.database = pymysql.connect(host=host,
                                            port=port,
                                            user=user,
                                            password=password,
                                            database=database)
            self.cursor = self.database.cursor()
            self.cursor.execute('SELECT VERSION()')
            log.info(f'Database Version:{self.cursor.fetchone()}')
            log.info('数据库连接成功')
        except Exception as e:
            log.critical('数据库连接失败')
            raise e

    def check_table_exist(self, table) -> None:
        '''
        判断表是否存在
        :param table: str 表名
        '''
        sql = "show tables"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        # print(tables)
        tables_list = re.findall('(\'.*?\')', str(tables))
        # print(tables_list)
        tables_list = [re.sub("'", '', each) for each in tables_list]
        # print(tables_list)
        if table not in tables_list:
            log.critical(f'{table}不存在')
            self.database.close()
            raise Exception

    def check_connection(self) -> None:
        '''
        确认连接未断开，否则重连
        '''
        try:
            self.database.ping(reconnect=False)
        except:
            log.warning('数据库重新连接')
            self.database.ping()
            self.cursor = self.database.cursor()

    def insert_data_into_mysql(self, table, data, condition='') -> None:
        '''
        写入数据到数据库
        :param table: str 表名
        :param data: tuple 值
        :param condition: str 条件
        '''
        self.check_connection()
        # self.check_table_exist(table)
        if condition == '':
            sql = f"""INSERT INTO {table}
         VALUES {data}"""
        else:
            sql = f"""INSERT INTO {table}
            VALUES {data} WHERE {condition}"""
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.database.commit()
            log.info(f'写入数据库成功{data}->{table}')
        except:
            # 如果发生错误则回滚
            self.database.rollback()
            log.critical(f'写入数据库{data}->{table}出错，已回滚')
            self.database.close()
            raise Exception

    def delete_data_from_mysql(self, table, condition) -> None:
        '''
        从数据库删除一条记录
        :param table: str 表名
        :param condition: str 条件
        '''
        sql = f'DELETE FROM {table} WHERE {condition}'
        try:
            self.cursor.execute(sql)
            self.database.commit()
            log.info(f'删除记录成功{table}-X{condition}')
        except:
            self.database.rollback()
            log.error(f'更新数据库失败，已回滚,sql:{sql}')
            raise Exception

    def update_data_into_mysql(self, table, set_data, condition) -> None:
        '''
        更新数据库信息
        :param table: str 表名
        :param set_data: str 赋值语句
        :param condition: str 条件
        '''
        self.check_connection()
        self.check_table_exist(table)
        sql = f'UPDATE {table} SET {set_data} WHERE {condition}'
        try:
            self.cursor.execute(sql)
            self.database.commit()
            log.info(f'更新数据库成功{condition}:{set_data}->{table}')
        except:
            self.database.rollback()
            log.error(f'更新数据库失败，已回滚,sql:{sql}')
            raise Exception

    def get_data_from_mysql(self, table, data_name ='*', condition=''):
        '''
        从数据库读取信息
        :param table: str 表名
        :param data_name: str 需要获取的字段名
        :param condition: str 条件
        :return:
        '''
        self.check_connection()
        self.check_table_exist(table)
        if condition == '':
            sql = f"""SELECT {data_name} FROM {table}"""
        else:
            sql = f"""SELECT {data_name} FROM {table} WHERE {condition}"""
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if data_name.find(',') == -1 and data_name != '*':
                new_data = []
                for i in data:
                    new_data.append((i[0]))
                data = tuple(new_data)
            if len(data) == 1 and condition != '':
                data = data[0]
            return data
        except:
            self.database.close()
            log.error(f'数据库读取信息失败,sql:{sql}')

            raise Exception

    def quit_database(self):
        self.database.close()
        log.info('已经关闭sql连接')

mysql = SqlAction()
if __name__ == '__main__':
    test = SqlAction()
    old = mysql.get_data_from_mysql('source_info','used_time',f"uuid='2cecba97f55ff992a3d5279a78cb3347'")
    mysql.update_data_into_mysql('source_info', f'used_time=0', f"uuid='2cecba97f55ff992a3d5279a78cb3347'")
    test.quit_database()