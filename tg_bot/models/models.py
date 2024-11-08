from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, BigInteger,DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class AccountsOz(Base):
    __tablename__ = 'accounts_oz'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Is_man = Column(Boolean)
    Path = Column(String)
    Path_id = Column(Integer)
    Date_active = Column(Date)
    Is_using = Column(Boolean)
    Date_reg = Column(Date)
    def __repr__(self):
        return (f"AccountsOz(Id={self.Id}, name={self.Name}, is_man={self.Is_man}, "
                f"path={self.Path}, path_id={self.Path_id}, date_active={self.Date_active}, "
                f"is_using={self.Is_using}, date_reg={self.Date_reg})")
class Order(Base): 
    __tablename__ = 'order'

    id = Column(BigInteger, primary_key=True)
    article = Column(BigInteger)
    search_key = Column(String) 
    size = Column(String) 
    account = Column(Integer)
    price = Column(Integer)
    buyer_id = Column(Integer)
    status = Column(Integer)
    date_buy = Column(DateTime)
    review_text = Column(Text)
    review_photo = Column(Text)  
    review_data = Column(DateTime)
    pvz = Column(Integer)
    marketplace = Column(Text)
    date_create = Column(DateTime) 
    date_get = Column(DateTime)
    brand = Column(Text)
    photo = Column(String) 
    sex = Column(Text) 
    name = Column(Text) 
    qr_code = Column(Text)  
    date_check = Column(DateTime)  
    date_check_get = Column(DateTime)
    status_buy = Column(Integer)
    status_warehouse = Column(Integer)
    status_delivery = Column(Integer)
    phone_buyer = Column(Text)  
    code = Column(Text)  
    text_status_delivery = Column(Text)  
    review_video = Column(Text) 
    def __repr__(self):
        return (f"YourTableName(id={self.id}, article={self.article}, search_key={self.search_key}, "
                f"size={self.size}, account={self.account}, price={self.price}, buyer_id={self.buyer_id}, "
                f"status={self.status}, date_buy={self.date_buy}, review_text={self.review_text}, "
                f"review_photo={self.review_photo}, review_data={self.review_data}, pvz={self.pvz}, "
                f"marketplace={self.marketplace}, date_create={self.date_create}, date_get={self.date_get}, "
                f"brand={self.brand}, photo={self.photo}, sex={self.sex}, name={self.name}, "
                f"qr_code={self.qr_code}, date_check={self.date_check}, date_check_get={self.date_check_get}, "
                f"status_buy={self.status_buy}, status_warehouse={self.status_warehouse}, "
                f"status_delivery={self.status_delivery}, phone_buyer={self.phone_buyer}, "
                f"code={self.code}, text_status_delivery={self.text_status_delivery})")
class User(Base): 
    __tablename__ = 'user' 
    username = Column(BigInteger, primary_key=True)
    id = Column(BigInteger) 
    password = Column(String)  
    email = Column(String) 
    first_name = Column(Text) 
    last_name = Column(Text) 
    is_active = Column(Boolean) 
    is_superuser = Column(Boolean)
    date_joined = Column(DateTime) 
    last_login = Column(DateTime)
    phone = Column(BigInteger) 
    money = Column(Integer) 
    who_added_last_money = Column(Integer)  
    is_registered = Column(Boolean)  
    is_authenticated = Column(Boolean)
    tg = Column(String) 
    def __repr__(self):
        return (f"User(username={self.username}, id={self.id}, password={self.password}, "
                f"email={self.email}, first_name={self.first_name}, last_name={self.last_name}, "
                f"is_active={self.is_active}, is_superuser={self.is_superuser}, "
                f"date_joined={self.date_joined}, last_login={self.last_login}, "
                f"phone={self.phone}, money={self.money}, who_added_last_money={self.who_added_last_money}, "
                f"is_registered={self.is_registered}, is_authenticated={self.is_authenticated}, tg={self.tg})")
                
def get_accounts_oz_class():
    return AccountsOz
def get_user_class():
    return User
def get_order_class():
    return Order

