from django.shortcuts import render
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from pymongo import MongoClient
from bson import ObjectId
from .firebase_config import firebase_admin
from firebase_admin import auth
import random


client = MongoClient('mongodb://localhost:27017/')
user_collection = client.test_db.users

def generate_username(email):
    username = email.split('@')[0]
    random_no = str(random.randint(1, 9999))
    username = f"{username}{random_no}"
    return username

@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if serializer.is_valid():
        if user_collection.find_one({'username': username}):
            response_data = {'error': 'A user with that username already exists'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if user_collection.find_one({'email': email}):
            response_data = {'error': 'A user with that email already exists'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            response_data = {'error': 'This password is too short. It must contain at least 8 characters'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if not email or not password:
            response_data = {'error': 'Email and password are required'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if (username and len(username) > 100) or len(email) > 100 or len(password) > 100 or (first_name and len(first_name) > 100) or (last_name and len(last_name) > 100):
            response_data = {'error': 'Only 100 characters are allowed for a field'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if not username:
            username = generate_username(email)

        user = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
        user_collection.insert_one(user)
        response_data = {
            'username': username,
            'email': email,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_data = user_collection.find_one({'username':username,'password':password})
        if user_data:
            custom_token = auth.create_custom_token(uid=str(user_data['_id']))
            serializer = UserLoginSerializer(user_data)
            response_data = {
                'username': user_data["username"],
                'email': user_data["email"],
                'full_name': serializer.data["full_name"],
                'custom_token': custom_token
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {'error': 'Username or password is invalid'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None

@api_view(['GET'])
def view(request):
    id_token = request.META.get('HTTP_AUTHORIZATION', '')
    decoded_token = verify_token(id_token)
    if decoded_token is None:
        return Response({'error': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)

    _id = decoded_token["uid"]
    user_data = user_collection.find_one({'_id': ObjectId(_id) })
    if user_data is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserLoginSerializer(user_data)
    full_name = serializer.data["full_name"],
    response_data = {
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'full_name': full_name,
    }

    return Response(response_data,  status=status.HTTP_200_OK)

@api_view(['POST'])
def edit(request):
    id_token = request.META.get('HTTP_AUTHORIZATION', '')
    decoded_token = verify_token(id_token)
    if decoded_token is None:
        return Response({'error': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)

    _id = decoded_token["uid"]
    user_data = user_collection.find_one({'_id': ObjectId(_id) })
    if user_data is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    
    check_user_exist = user_collection.find_one({'username': username})

    if check_user_exist is not None:
        return Response({'detail': f'User already exists with the username {username}'}, status=status.HTTP_409_CONFLICT)

    if first_name is not None:
        user_data['first_name'] = first_name
    if last_name is not None:
        user_data['last_name'] = last_name
    if username is not None:
        user_data['username'] = username
    user_collection.update_one({'_id': user_data['_id']}, {'$set': user_data})

    serializer = UserLoginSerializer(user_data)
    full_name = serializer.data["full_name"],
    response_data = {
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'full_name': full_name,
    }

    return Response(response_data,  status=status.HTTP_200_OK)