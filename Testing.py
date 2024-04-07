import jwt
import datetime

# User data
user_data = {
    "name": "John Doe",
    "uid": "123456",
    "phone": "1234567890",
    "age": 30,
    "password": "password123"
}

# Include 'exp' field with current time + 30 minutes
user_data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

# Secret key (replace with your actual key)
SECRET_KEY = "4L)Ax@j7*_Dingle_Dangle_@mp$mQ&%h2Q"

# Encode user data into a JWT token
token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')

print(token)