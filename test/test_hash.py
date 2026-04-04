import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.hash_utils import generate_file_hash

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(base_dir, "data", "falcon_jan.xlsx")

with open(file_path, "rb") as f:
    print(generate_file_hash(f))
