import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import Base, engine
from app.models import *

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
