from database import Base
from sqlalchemy import Integer, String, Column, ForeignKey,Boolean
from basemodel import templatemodel
import logging
from database import SessionLocal
from telegram import user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class User(Base):
	__tablename__="users"
	user_id = Column(Integer,primary_key=True)
	portfolio = Column(String)
	watchlist = Column(String)
	is_subscribed = Column(Boolean,default=True)

	

	temp = Column
	teamp = Column

	def __repr__(self):
		return "<User(user_id='%s', portfolio='%s', watchlist='%s', " "is_subscribed='%s')>" % (self.user_id, self.portfolio,self.watchlist, self.is_subscribed)

	def __call__(self):
		return {
			"portfolio":self.portfolio,
			"watchlist":self.watchlist,
			"is_subscribed":self.is_subscribed
		}
	
	def get_user(session:SessionLocal,userid:int):
		"""Queries a user from database
		Args:
		user_id(int): User's telegram id

		Returns:
		Users:Instance of User class
		"""
		logger.info(f"Retrieving user info for user{userid}")
		curr_user = session.query(User).filter_by(user_id=userid).first()

		# Prepare a ne User object if the user is not found in DB
		if not curr_user:
			return User(user_id=userid,portfolio="[]",watchlist="[]")
		return curr_user

	def update_userdb(session:SessionLocal,User:user)->None:
		""" Creates a User object within session before commit()
		Args:
			user_id(int):User's telegram ID
		"""
			
		try:
			session.add(User)
			session.commit()
			logger.info(f"Successfully updated db with {User} ")
		except Exception as e:
			logger.error(f"{e}")

	def get_subscribers(session:SessionLocal):
		subscribers = session.query(User).filter_by(is_subscribed=True).all()
		return subscribers
	
	def unsubscribe_user(session: SessionLocal, User: user) -> None:
		"""
		Unsubscribe a user if he/she has removed the bot from the Telegram application
		"""
		session.query(User).filter_by(user_id=user.user_id).update({"is_subscribed": False  })
		session.commit()


class strategy(Base):
	__tablename__ = "strategy"
	id = Column(Integer, primary_key=True, index = True)
	name = Column(String, index=True, unique= True)

class stock_strategy(Base):
	__tablename__ = "stock_strategy"
	stock_id = Column(Integer,primary_key=True)
	stategy_id = Column(Integer, ForeignKey("strategy.id"))


class mainmarket_list (Base):
	__tablename__ = "mainmarket_list"
	id = Column(Integer, primary_key=True, index=True)
	Instrument_Code = Column(String, index=True, unique = True)
	Name = Column(String)
	Currency = Column(String)
	Sector = Column(String)
	Type = Column(String)
	Sentiment = Column(String)

class juniormarket_list (Base):

	__tablename__ = "juniormarket_list"
	id = Column(Integer, primary_key=True, index=True)
	Instrument_Code = Column(String, index=True, unique = True)
	Name = Column(String)
	Currency = Column(String)
	Sector = Column(String)
	Type = Column(String)
	Sentiment = Column(String)


class stock_AFS (templatemodel,Base):
	__tablename__ = "stock_AFS"

class stock_AMG (templatemodel,Base):
	__tablename__ = "stock_AMG"

class stock_BPOW (templatemodel,Base):
	__tablename__ = "stock_BPOW"

class stock_CAC (templatemodel,Base):
	__tablename__ = "stock_CAC"

class stock_CHL (templatemodel,Base):
	__tablename__ = "stock_CHL"

class stock_CABROKERS (templatemodel,Base):
	__tablename__ = "stock_CABROKERS"

class stock_KREMI (templatemodel,Base):
	__tablename__ = "stock_KREMI"

class stock_CFF (templatemodel,Base):
	__tablename__ = "stock_CFF"

class stock_PURITY (templatemodel,Base):
	__tablename__ = "stock_PURITY"

class stock_DTL (templatemodel,Base):
	__tablename__ = "stock_DTL"

class stock_DCOVE (templatemodel,Base):
	__tablename__ = "stock_DCOVE"

class stock_ELITE (templatemodel,Base):
	__tablename__ = "stock_ELITE"

class stock_EFRESH (templatemodel,Base):
	__tablename__ = "stock_EFRESH"

class stock_ECL (templatemodel,Base):
	__tablename__ = "stock_ECL"

class stock_FTNA (templatemodel,Base):
	__tablename__ = "stock_FTNA"

class stock_FOSRICH (templatemodel,Base):
	__tablename__ = "stock_FOSRICH"

class stock_FESCO (templatemodel,Base):
	__tablename__ = "stock_FESCO"

class stock_GENAC (templatemodel,Base):
	__tablename__ = "stock_GENAC"

class stock_GWEST (templatemodel,Base):
	__tablename__ = "stock_GWEST"

class stock_HONBUN (templatemodel,Base):
	__tablename__ = "stock_HONBUN"

class stock_ICREATE (templatemodel,Base):
	__tablename__ = "stock_ICREATE"

class stock_INDIES (templatemodel,Base):
	__tablename__ = "stock_INDIES"

class stock_ROC (templatemodel,Base):
	__tablename__ = "stock_ROC"

class stock_ISP (templatemodel,Base):
	__tablename__ = "stock_ISP"

class stock_JAMT (templatemodel,Base):
	__tablename__ = "stock_JAMT"

class stock_JETCON (templatemodel,Base):
	__tablename__ = "stock_JETCON"

class stock_KLE (templatemodel,Base):
	__tablename__ = "stock_KLE"

class stock_KEX (templatemodel,Base):
	__tablename__ = "stock_KEX"

class stock_LASD (templatemodel,Base):
	__tablename__ = "stock_LASD"

class stock_LASF (templatemodel,Base):
	__tablename__ = "stock_LASF"

class stock_LASM (templatemodel,Base):
	__tablename__ = "stock_LASM"

class stock_LUMBER (templatemodel,Base):
	__tablename__ = "stock_LUMBER"

class stock_MAILPAC (templatemodel,Base):
	__tablename__ = "stock_MAILPAC"

class stock_MEEG (templatemodel,Base):
	__tablename__ = "stock_MEEG"

class stock_MDS (templatemodel,Base):
	__tablename__ = "stock_MDS"

class stock_PTL (templatemodel,Base):
	__tablename__ = "stock_PTL"

class stock_SSLVC (templatemodel,Base):
	__tablename__ = "stock_SSLVC"

class stock_SOS (templatemodel,Base):
	__tablename__ = "stock_SOS"

class stock_LAB (templatemodel,Base):
	__tablename__ = "stock_LAB"

class stock_TROPICAL (templatemodel,Base):
	__tablename__ = "stock_TROPICAL"

class stock_TTECH (templatemodel,Base):
	__tablename__ = "stock_TTECH"

class stock_138SL (templatemodel,Base):
	__tablename__ = "stock_138SL"

class stock_1834 (templatemodel,Base):
	__tablename__ = "stock_1834"

class stock_BIL (templatemodel,Base):
	__tablename__ = "stock_BIL"

class stock_BRG (templatemodel,Base):
	__tablename__ = "stock_BRG"

class stock_CCC (templatemodel,Base):
	__tablename__ = "stock_CCC"

class stock_CPJ (templatemodel,Base):
	__tablename__ = "stock_CPJ"

class stock_CAR (templatemodel,Base):
	__tablename__ = "stock_CAR"

class stock_CBNY (templatemodel,Base):
	__tablename__ = "stock_CBNY"

class stock_CPFV (templatemodel,Base):
	__tablename__ = "stock_CPFV"

class stock_EPLY (templatemodel,Base):
	__tablename__ = "stock_EPLY"

class stock_FIRSTROCKJMD (templatemodel,Base):
	__tablename__ = "stock_FIRSTROCKJMD"

class stock_GK (templatemodel,Base):
	__tablename__ = "stock_GK"

class stock_GHL (templatemodel,Base):
	__tablename__ = "stock_GHL"

class stock_JBG (templatemodel,Base):
	__tablename__ = "stock_JBG"

class stock_JP (templatemodel,Base):
	__tablename__ = "stock_JP"

class stock_JSE (templatemodel,Base):
	__tablename__ = "stock_JSE"

class stock_JMMBGL (templatemodel,Base):
	__tablename__ = "stock_JMMBGL"

class stock_KEY (templatemodel,Base):
	__tablename__ = "stock_KEY"

class stock_KPREIT (templatemodel,Base):
	__tablename__ = "stock_KPREIT"

class stock_KW (templatemodel,Base):
	__tablename__ = "stock_KW"

class stock_MTL (templatemodel,Base):
	__tablename__ = "stock_MTL"

class stock_MIL (templatemodel,Base):
	__tablename__ = "stock_MIL"

class stock_MJE (templatemodel,Base):
	__tablename__ = "stock_MJE"

class stock_MPCCEL (templatemodel,Base):
	__tablename__ = "stock_MPCCEL"

class stock_NCBFG (templatemodel,Base):
	__tablename__ = "stock_NCBFG"

class stock_PAL (templatemodel,Base):
	__tablename__ = "stock_PAL"

class stock_PJAM (templatemodel,Base):
	__tablename__ = "stock_PJAM"

class stock_PJX (templatemodel,Base):
	__tablename__ = "stock_PJX"

class stock_PROVEN (templatemodel,Base):
	__tablename__ = "stock_PROVEN"

class stock_PULS (templatemodel,Base):
	__tablename__ = "stock_PULS"

class stock_QWI (templatemodel,Base):
	__tablename__ = "stock_QWI"

class stock_RJR (templatemodel,Base):
	__tablename__ = "stock_RJR"

class stock_SJ (templatemodel,Base):
	__tablename__ = "stock_SJ"

class stock_XFUND (templatemodel,Base):
	__tablename__ = "stock_XFUND"

class stock_SELECTF (templatemodel,Base):
	__tablename__ = "stock_SELECTF"

class stock_SELECTMD (templatemodel,Base):
	__tablename__ = "stock_SELECTMD"

class stock_SALF (templatemodel,Base):
	__tablename__ = "stock_SALF"

class stock_SGJ (templatemodel,Base):
	__tablename__ = "stock_SGJ"

class stock_SEP (templatemodel,Base):
	__tablename__ = "stock_SEP"

class stock_SML (templatemodel,Base):
	__tablename__ = "stock_SML"

class stock_SIL (templatemodel,Base):
	__tablename__ = "stock_SIL"

class stock_SVL (templatemodel,Base):
	__tablename__ = "stock_SVL"

class stock_SCIJMD (templatemodel,Base):
	__tablename__ = "stock_SCIJMD"

class stock_SCIUSD (templatemodel,Base):
	__tablename__ = "stock_SCIUSD"

class stock_SRFJMD (templatemodel,Base):
	__tablename__ = "stock_SRFJMD"

class stock_TJH (templatemodel,Base):
	__tablename__ = "stock_TJH"

class stock_VMIL (templatemodel,Base):
	__tablename__ = "stock_VMIL"

class stock_WIG (templatemodel,Base):
	__tablename__ = "stock_WIG"

class stock_WISYNCO (templatemodel,Base):
	__tablename__ = "stock_WISYNCO"