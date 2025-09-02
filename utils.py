from passlib.context import CryptContext
crypt_pass_make = CryptContext(schemes = ["bcrypt"], deprecated= "auto")

def hash(password:str):
    password_encrypt = crypt_pass_make.hash(password)
    return password_encrypt

def verify(plain_password, hashed_password):
    return crypt_pass_make.verify(plain_password, hashed_password)

