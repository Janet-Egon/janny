
from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from . import serializers
from . import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
import jwt  
from django.db.models import Q


def generate_access_token(user):        
    payload ={
        'user_id' : user.id,
        'exp' : datetime.utcnow() + timedelta(minutes=5),   
        'iat' :  datetime.utcnow()             
    }    
    access_token = jwt.encode(payload, 'secret', algorithm='HS256')
    
    return access_token
    
class Signup(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data['username']
            if models.User.objects.filter(username=user_name).exists():
                return Response({'error': 'Username already exists'})
            serializer.save(
                password=make_password(serializer.validated_data['password']),
            )
            return Response({'message': 'account has been created successfuly'})
                                       
        else:
            return Response({'error': serializer.errors})
                
class Login(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data = request.data)   
        if serializer.is_valid(): 
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data['password']
            try:
                logged_user = models.User.objects.get(username=user_name)
            except Exception as e:   
                return Response({"message" : str(e)},)    
            password_check = check_password(pass_word, logged_user.password)
            if password_check :
                token = generate_access_token(logged_user)
                response = Response()
                response.set_cookie('access_token', value=token, httponly=True)
                response.data = {
                    'message' : 'login success',
                    'access_token' : token
                }
                return response
            return Response({'error' : 'Invalid username or password'})
        
        # else: 
            # return Response({"error": serializer.errors})

class CreatePost(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message' : 'unautheticated'})
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e: 
            return Response({'error': str(e)})
        try : 
            logged_user = models.User.objects.get(id=payload['user_id'])
            if not logged_user :
             return Response({'message' : 'only user can make post'})
        except Exception as e:
            return Response({'error': str(e)},)
        serializer = serializers.PostSerializer(data = request.data)   
        if serializer.is_valid():
            serializer.save(author=logged_user)
            return Response({'message' : 'post created successfully'}) 
        return Response({'message' : 'serializer is not valid', 'error' : serializer.errors})

class View(APIView):
   def get(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message' : 'unautheticated'})
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e: 
            return Response({'error': str(e)})
        
        try:
            logged_user = models.User.objects.get(id=payload['user_id'])
            if not logged_user:
                return Response({'message': 'post not found'})
        except Exception :
            return Response({'error' : str(e)})

        posts = models.Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True)
        return Response({'message': serializer.data})   

class Update(APIView):
    def put(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message' : 'unautheticated'})
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e: 
            return Response({'error': str(e)})
        try : 
            logged_user = models.User.objects.get(id=payload['user_id'])
            if not logged_user :
             return Response({'message' : 'only user can make post'})
        except Exception as e:
            return Response({'error': str(e)},)
        serializer = serializers.PostSerializer(data = request.data)   
        if serializer.is_valid():
            serializer.save(author=logged_user)
            return Response({'message' : 'post updated successfully'}) 
        return Response({'message' : 'serializer is not valid', 'error' : serializer.errors})
 

class Delete(APIView):
    def delete(self,request):
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message' : 'unautheticated'})
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e: 
            return Response({'error': str(e)})
        try : 
            logged_user = models.User.objects.get(id=payload['user_id'])
            if not logged_user :
             return Response({'message' : 'only user can make post'})
        except Exception as e:
            return Response({'error': str(e)},)
        serializer = serializers.PostSerializer(data = request.data)   
        if serializer.is_valid():
            serializer.save(author=logged_user)
            return Response({'message' : 'post deleted successfully'}) 
        return Response({'message' : 'serializer is not valid', 'error' : serializer.errors})
 




