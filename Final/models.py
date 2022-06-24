from sqlalchemy import Column, Integer, String, Float, Boolean
import db

class Users(db.Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    passwd = Column(String, nullable=False)
    rol = Column(String, nullable=False)

    def __init__(self, name, passwd, rol):
        self.name = name
        self.passwd = passwd
        self.rol = rol

    def __str__(self):
        return "{} / {}".format(self.name, self.rol)


class Products(db.Base):

    __tablename__ = "products"

    code = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)

    def __init__(self, code, name, stock, purchase_price, sale_price):
        self.code = code
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.sale_price = sale_price

    def __str__(self):
        return "{} - {} UNIDADES - PRECIO VENTA: ${}".format(self.name, self.stock, self.sale_price)

class Tickets(db.Base):

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numticket = Column(Integer, nullable=False)
    code = Column(Integer, nullable=False)
    cant = Column(Integer, nullable=False)
    desc = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    totalprice = Column(Float, nullable=False)
    paid = Column(Boolean, nullable=False)

    def __init__(self, numticket, code, cant, desc, price, totalprice, paid):
        self.numticket = numticket
        self.code = code
        self.cant = cant
        self.desc = desc
        self.price = price
        self.totalprice = totalprice
        self.paid = paid


    def __str__(self):
        return "{} - cant: {} - {} / ${}".format(self.numticket, self.cant, self.desc, self.totalprice)