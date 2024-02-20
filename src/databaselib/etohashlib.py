import pyargon2
import random
import string

iterations_time_cost = 640

def generateSaltHash(password:str) -> str:
    
    # Define the password to be hashed
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    # Hash the password using pyArgon2
    hashed_password = pyargon2.hash(password, salt, time_cost=iterations_time_cost)
    return (hashed_password, salt)

def checkPassword(hashed_password:str, password_to_verify:str, salt_to_verify:str) -> bool:

    hash_to_verify = pyargon2.hash(password_to_verify, salt_to_verify, time_cost=iterations_time_cost)

    if hashed_password == hash_to_verify:
        return True
    return False