from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str: # хэширование пароля
    return password_hash.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool: # проверка пароля с уже хэшированным 
    return password_hash.verify(plain_password, hashed_password)
