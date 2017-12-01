import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Asset(Base):
    __tablename__   = 'asset'
    id              = Column(Integer, primary_key = True)
    type            = Column(String(10), nullable = False)
    exchange        = Column(String(10), nullable = False) # NASDAQ, CME, CBOE, NYSE
    symbol          = Column(String(20), nullable = False) # security symbol or bond cusip
    description     = Column(String(20), nullable = False)
    size            = Column(Integer)                       # contract size; stock = $1, S&P 500 e-mini = $50, vix = $1000
    def __repr__(self):
        return("\n\tasset id: {0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.type, self.exchange, self.symbol, self.description, self.size))

class Allocation(Base):
    __tablename__   = 'allocation'
    id              = Column(Integer, primary_key = True)
    date_mod        = Column(String(28), nullable = False)
    portfolio       = Column(String(10), nullable = False)          # use a string name for portfolio
    asset_id        = Column(Integer, ForeignKey('asset.id'))
    asset           = relationship(Asset)
    allocation      = Column(Float, nullable = False)
    def __repr__(self):
        return("\n\tallocation id: {0}\t{1}\t{2}\t{3}\t{4:.2%}".format(self.id, self.portfolio, self.asset_id, self.asset, self.allocation))

## insert at end of file ##
engine = create_engine('sqlite:///simco.db')
#Base.metadata.create_all(engine)        # suppress this if creating DB via SQL script?
