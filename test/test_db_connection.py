import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.database_connection import test_connection

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_connection()
