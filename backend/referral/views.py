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
    expiration_time = timedelta(days=3)

    def get(self, request):
        # Retrieve the token from the query parameter
        cur_token = request.query_params.get('token')

        try: 
            if cur_token:
                # Check if the token exists in Redis
                user_id = redis_client.hget('tokens', cur_token)

                if user_id:
                    user_id = int(user_id.decode('utf-8'))
                    token_created = float(cur_token.split(":")[-1])  # Extract the token creation timestamp
                    current_time = datetime.now().timestamp()

                    # Check if the token has expired
                    if token_created + self.expiration_time.total_seconds() < current_time:
                        # Token has expired, delete it from Redis
                        redis_client.hdel('tokens', cur_token)
                        return Response({'error': "Session times out! Please sign in again"}, status=401)

                    for student in Student.objects.all():
                        if student.user.id == user_id:
                            return Response({'student_id': student.id, 'user_id': user_id, 'username': student.user.username, 'email': student.user.email})
                    for alumni in Alumni.objects.all():
                        if alumni.user.id == user_id:
                            return Response({'alumni_id': alumni.id, 'user_id': user_id, 'username': alumni.user.username, 'email': alumni.user.email})
                    raise ValueError('The user is not found')
                else:
                    return Response({'error': "Invalid Token"}, status=401)
                
        except Exception as e:
                return Response({'error': str(e)}, status=500)
        

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                # Generate a unique token
                random_component = binascii.hexlify(os.urandom(20)).decode()
                token = f'{random_component}:{datetime.now().timestamp()}'

                # Store the token in Redis with an expiration time
                redis_client.hsetnx('tokens', token, str(user.id))
                redis_client.expire(token, int(self.expiration_time.total_seconds()))

                return Response({'token': token, 'expiration': str(datetime.now() + self.expiration_time)})
            else:
                return Response({'error': 'Unauthorized user'}, status=401)

        return Response({'error': 'Invalid request'}, status=400)
