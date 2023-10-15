import traceback
import redis
import os
import binascii
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from user.models import Student, Alumni
from datetime import timedelta, datetime
from django.conf import settings

# Initialize a Redis client
redis_client = settings.REDIS_CLIENT

class ObtainTokenView(APIView):
    def get(self, request):
        # Retrieve the token from the query parameter
        cur_token = request.query_params.get('token')
        # print(cur_token)
        try: 
            if cur_token:
                # Check if the token exists in Redis
                id = redis_client.get(cur_token)
                if not id:
                    raise ValueError('Session Time Out! Please log in again') 
                user_id = int(id)
                if user_id:
                    for student in Student.objects.all():
                        if student.user.id == user_id:
                            return Response({'student_id': student.id, 'user_id': user_id, 'username': student.user.username, 'email': student.user.email})
                    for alumni in Alumni.objects.all():
                        if alumni.user.id == user_id:
                            return Response({'alumni_id': alumni.id, 'user_id': user_id, 'username': alumni.user.username, 'email': alumni.user.email})
                    raise ValueError('The user is not found')
                else:
                    return Response({'error': "Invalid Token"}, status=401)
            else:
                raise ValueError('Session Time Out! Please log in again')
                
        except Exception as e:
                traceback.print_exc()
                return Response({'error': str(e)}, status=500)
        

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                # Generate a unique token
                token = binascii.hexlify(os.urandom(20)).decode()
                # Store the token in Redis with an expiration time
                redis_client.set(token, str(user.id))
                redis_client.expire(token, 60 * 60)

                return Response({'token': token})
            else:
                return Response({'error': 'Unauthorized user'}, status=401)

        return Response({'error': 'Invalid request'}, status=400)
