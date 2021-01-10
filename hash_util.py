import hashlib
import json

def hash_string_256(string):
  return hashlib.sha256(string).hexdigest()

# ----------------------------------------------------
# function to create hashed block
def create_hash_block(block):
    # hash the block and convert to string with json library and encode to utf-8 and hexdigest to have normal characters
    # Because a dictionary is unordered, we order the keys before convert the block to string
    hash_block = hash_string_256(json.dumps(block, sort_keys=True).encode())
    return hash_block