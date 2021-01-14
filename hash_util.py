import hashlib
import json

def hash_string_256(string):
  return hashlib.sha256(string).hexdigest()

# ----------------------------------------------------
# function to create hashed block
def create_hash_block(block):
    # hash the block and convert to string with json library and encode to utf-8 and hexdigest to have normal characters
    # Convert the block object to a copy of a dictionary
    hashable_block = block.__dict__.copy()
    hash_block = hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
    return hash_block