
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, DATETIME

from data_model.db import DbHandler

Base = declarative_base()

class T_Base():
    db_hdl = DbHandler()
    def __init__():
        self.db_hdl = DbHandler()


class T_Basic_ShopBook(Base, T_Base):
    __tablename__ = 'T_BASIC_SHOPBOOK'

    id = Column(Integer, primary_key=True)
    book = Column(String(20))
    shop = Column(String(20))
    url = Column(String(1024))

    @classmethod
    def add(cls, shop, book, url):
        r = cls.db_hdl.session.query(cls.id).filter(cls.shop==shop, cls.book==book).first()
        if r is not None:
            return

        cls.db_hdl.session.add(cls(shop=shop, book=book, url=url))
        cls.db_hdl.session.commit()

    @classmethod
    def query_shopbook_id(cls, shop, book):
        # r = cls.db_hdl.session.query(cls.id).filter('shop'==shop, 'book'==book).first()
        r = cls.db_hdl.session.query(cls.id).filter(cls.shop==shop, cls.book==book).first()
        return r

    @classmethod
    def query_book_list(cls, shop):
        # r = cls.db_hdl.session.query(cls.id).filter('shop'==shop, 'book'==book).first()
        r = cls.db_hdl.session.query(cls.book).filter(cls.shop==shop).all()
        return [i[0] for i in r]

    @classmethod
    def query_url_list(cls):
        # r = cls.db_hdl.session.query(cls.id).filter('shop'==shop, 'book'==book).first()
        r = cls.db_hdl.session.query(cls.url).filter().all()
        return [i[0] for i in r]


class T_Data(Base, T_Base):
    __tablename__ = 'T_DATA'

    # sb_id = Column(Integer, primary_key=True)
    shop = Column(String(20), primary_key=True)
    book = Column(String(20), primary_key=True)
    datatype = Column(String(20), primary_key=True)
    value = Column(Integer)
    date = Column(DATETIME, primary_key=True)

    @classmethod
    def add(cls, shop, book, datatype, date, value):
        cls.db_hdl.session.add(cls(shop=shop, book=book, datatype=datatype, date=date, value=value))
        cls.db_hdl.session.commit()

    # datatype_value_list, [('price', 85), ]
    @classmethod
    def add_bundle(cls, shop, book, date, datatype_value_list):
        values = []
        for datatype_value in datatype_value_list:
            values.append(cls(shop=shop, book=book, date=date, datatype=datatype_value[0], value=datatype_value[1]))
        cls.db_hdl.session.bulk_save_objects(values)
        cls.db_hdl.session.commit()

    @classmethod
    def query(cls, shop, book, datatype, start, end):
        r = cls.db_hdl.session.query(cls.date, cls.value).filter(cls.shop==shop, cls.book==book, cls.datatype==datatype, cls.date>=start, cls.date<end).all()
        return r

    @classmethod
    def query_anyshop_anytype(cls, book, start, end):
        # print(book, start, end)
        # q = cls.db_hdl.session.query(cls.shop, cls.datatype, cls.date, cls.value).filter(cls.book==book, cls.date>=start, cls.date<end)
        # r = q.all()
        # print(q)

        # r = cls.db_hdl.session.query(cls.shop, cls.datatype, func.concat(cls.date), cls.value).filter(cls.book==book, cls.date>=start, cls.date<end).all()
        # r = cls.db_hdl.session.query(cls.shop, cls.datatype, func.concat(func.DATE(cls.date)), cls.value).filter(cls.book==book, cls.date>=start, cls.date<end).all()
        r = cls.db_hdl.session.query(cls.shop, cls.datatype, cls.value).filter(cls.book==book, cls.date>=start, cls.date<end).all()
        return r
