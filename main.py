from flask import Flask, request, jsonify
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)

app = FastAPI()
fake_users_db: Dict[str, str] = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
A Pydantic model representing a user schema, with fields for username and password.
"""
class UserSchema(BaseModel):
    username: str
    password: str
    
"""
A Pydantic model representing a payload with a list of integers and a target integer.
"""    
class Payload(BaseModel):
        numbers: List[int]

"""
A Pydantic model representing a payload for a binary search operation, with a list of integers and a target integer.
"""
class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

SECRET_KEY = "tu_clave_secreta_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Creates a new access token with the provided data and the configured expiration time.
#     Args:
#         data (dict): A dictionary containing the data to be encoded in the access token.
#     Returns:
#         str: The encoded JWT access token.
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Hashes the provided password using the configured password hashing context.
#     Args:
#         password (str): The plaintext password to be hashed.
#     Returns:
#         str: The hashed password.
def get_password_hash(password: str):
        return pwd_context.hash(password)

# Verifies a plaintext password against a hashed password using the configured password hashing context.
#     Args:
#         plain_password (str): The plaintext password to be verified.
#         hashed_password (str): The hashed password to compare against.
#     Returns:
#         bool: True if the plaintext password matches the hashed password, False otherwise.
def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

# Verifies a JWT token using the configured secret key and algorithm.
    
#     Args:
#         token (str): The JWT token to be verified.
    
#     Returns:
#         dict: The decoded payload of the JWT token, or None if the token is invalid or expired.
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None


    ...
# Registers a new user with the provided user data.
#
# Args:
#     user (UserSchema): The user data to be registered.
#
# Raises:
#     HTTPException: If the username already exists in the fake_users_db.
#
# Returns:
#     dict: A message indicating that the user was registered successfully.  
@app.post("/register")
async def register(user: UserSchema):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )
    
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = hashed_password
    
    return {"message": "User registered successfully"}


# Authenticates a user and generates an access token.
#
# Args:
#     user (UserSchema): The user data to be authenticated.
#
# Raises:
#     HTTPException: If the username is not found in the fake_users_db or the password is invalid.
#
# Returns:
#     dict: The generated access token.
@app.post("/login")
async def login(user: UserSchema):
    if user.username not in fake_users_db:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )
    
    stored_password = fake_users_db[user.username]
    if not verify_password(user.password, stored_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )
    
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}

# Verifies the provided token and returns the decoded payload.
#
# Args:
#     token (str): The token to be verified.
#
# Raises:
#     HTTPException: If the token is invalid or expired.
#
# Returns:
#     dict: The decoded payload of the verified token.
def verify_token_dependency(token: str):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )
    return payload

# Applies the bubble sort algorithm to the provided list of numbers.
#
# Args:
#     payload (Payload): The payload containing the list of numbers to be sorted.
#     token (str): The access token to be verified.
#
# Returns:
#     dict: The sorted list of numbers.
@app.post("/bubble-sort")
async def bubble_sort_endpoint(payload: Payload, token: str):
    verify_token_dependency(token)
    numbers = payload.numbers.copy()
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return {"numbers": numbers}

# Filters the provided list of numbers to only include even numbers.
#
# Args:
#     payload (Payload): The payload containing the list of numbers to be filtered.
#     token (str): The access token to be verified.
#
# Returns:
#     dict: The list of even numbers.
@app.post("/filter-even")
async def filter_even_endpoint(payload: Payload, token: str):
    verify_token_dependency(token)
    numbers = payload.numbers
    even_numbers = [num for num in numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}

# Calculates the sum of the elements in the provided list of numbers.
#
# Args:
#     payload (Payload): The payload containing the list of numbers.
#     token (str): The access token to be verified.
#
# Returns:
#     dict: The sum of the elements in the list.
@app.post("/sum-elements")
async def sum_elements_endpoint(payload: Payload, token: str):
    verify_token_dependency(token)
    numbers = payload.numbers
    total_sum = sum(numbers)
    return {"sum": total_sum}
# Finds the maximum value in the provided list of numbers.
#
# Args:
#     payload (Payload): The payload containing the list of numbers.
#     token (str): The access token to be verified.
#
# Returns:
#     dict: The maximum value in the list.
@app.post("/max-value")
async def max_value_endpoint(payload: Payload, token: str):
    verify_token_dependency(token)
    numbers = payload.numbers
    max_number = max(numbers)
    return {"max": max_number}

# Performs a binary search on the provided list of numbers to find the target value.
#
# Args:
#     payload (BinarySearchPayload): The payload containing the list of numbers and the target value.
#     token (str): The access token to be verified.
#
# Returns:
#     dict: A dictionary indicating whether the target value was found and its index.
@app.post("/binary-search")
async def binary_search_endpoint(payload: BinarySearchPayload, token: str):
    verify_token_dependency(token)
    numbers = payload.numbers
    target = payload.target
    
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return {"found": False, "index": -1}