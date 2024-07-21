import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URL : str = os.getenv("URL")

engine = create_engine(URL, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()