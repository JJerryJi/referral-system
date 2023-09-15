from typing import Any
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from user.models import Student, Alumni
from django.utils import timezone
from datetime import timedelta, datetime


class ObtainTokenView(APIView):
    expiration_time = timedelta(days=3)

    def get(self, request):
        # Retrieve the token from query parameters
        cur_token = request.query_params.get('token')
        user = None
        for token in Token.objects.all():
            if cur_token == str(token.key):
                # check if the token is still valid:
                if token.created + self.expiration_time < timezone.now():
                    # if session timeout, delete this token
                    token.delete()
                    return Response({'error': "Session times out! Plz sign in again"}, status=401)
                user = token.user
        if not user:
            return Response({'error': "Invalid Token"}, status=404)
        for student in Student.objects.all():
            if student.user == user:
                return Response({'student_id': student.id, 'user_id': user.id, 'username': user.username, 'email': user.email})
        for alumni in Alumni.objects.all():
            if alumni.user == user:
                return Response({'alumni_id': alumni.id, 'user_id': user.id, 'username': user.username, 'email': user.email})
        return Response({'error': 'no user information found'}, status=404)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # print(username, password)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                token.save()
                # Use 'token.key' to access the token key
                return Response({'token': token.key, 'expiration': token.created + self.expiration_time})
        return Response({'error': 'Unauthorized user'}, status=400)
