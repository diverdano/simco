#import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class RefData(object):
    ''' reference data, couple be moved to DB if needed '''
    secType             = ['equity','option','future','bond']
    exchange            = ['NASDAQ','CME','CBOE','NYSE','OTC']

class Asset(Base):
    __tablename__   = 'asset'
    id              = Column(Integer, primary_key = True, autoincrement = True)
    type            = Column(String(10), nullable = False)  # equity, option, future, bond
    exchange        = Column(String(10), nullable = False)  # NASDAQ, CME, CBOE, NYSE
    symbol          = Column(String(20), nullable = False)  # security symbol or bond cusip
    description     = Column(String(20), nullable = False)
    size            = Column(Integer, nullable = False)     # contract size; stock = $1, S&P 500 e-mini = $50, vix = $1000
    coupon          = Column(Float)                         # only for bonds
    expiry          = Column(String(25))                    # for equity options, futures, 'maturity' for bonds
    strike          = Column(Integer)                       # for options
    def __repr__(self):
        return("\n\tasset id: {0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.type, self.exchange, self.symbol, self.description, self.size))

class Allocation(Base):
    __tablename__   = 'allocation'
    id              = Column(Integer, primary_key = True, autoincrement = True)
    date_mod        = Column(String(25), nullable = False)
    portfolio       = Column(String(10), nullable = False)          # use a string name for portfolio
    asset_id        = Column(Integer, ForeignKey('asset.id'))
    asset           = relationship(Asset)
    allocation      = Column(Float, nullable = False)
    def __repr__(self):
#        return("\n\tallocation id: {0}\t{1}\t{2}\t{3}\t{4:.2%}".format(self.id, self.portfolio, self.asset_id, self.asset, self.allocation))
        return("\n\tallocation id: {0}\t{1}\t{2}\t{3}\t{4:.2%}".format(self.id, self.portfolio, self.asset_id, self.asset, self.allocation))

## insert at end of file ##
def createDBsession(db_info):
    ''' create session to db '''
    return sessionmaker()(bind=create_engine(db_info))
#engine = create_engine('sqlite:///simco.db')
#Base.metadata.create_all(engine)        # suppress this if creating DB via SQL script?
