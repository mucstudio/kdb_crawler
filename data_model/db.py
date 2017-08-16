
import datetime

import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from util.log import logger
from helper.config import ConfigHelper
# from data_model.table import T_Project


class DbHandler:
    def __init__(self):
        self.init_engine()
        self.init_session()

    def __del__(self):
        self.close_session()

    def init_engine(self):
        conn_info = ConfigHelper.get_mysql_conn_info()
        print(conn_info)
        #self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8&unix_socket={5}".format(
        self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
            conn_info['user'],
            conn_info['passwd'],
            conn_info['ip'],
            conn_info['port'],
            conn_info['db'],
            # conn_info['sock'],
        ), echo=False)

    def init_session(self):
        Session = sessionmaker(bind=self.engine)
        #将创建的数据库连接关联到这个session
        #Session.configure(bind=engine)
        self.session = Session()

    def close_session(self):
        self.session.close()

    def query(self, sql):
        #logger.debug(sql)
        return self.session.execute(sql).fetchall()


if __name__ == '__main__':
    db = DbHandler()
    r = db.session.execute('select * from T_COMP_INFO;')
    #db.add_start_plus_step('group_1')
    #r = db.query_start_plus_step('group_1', 1)
    print(r.fetchall())
