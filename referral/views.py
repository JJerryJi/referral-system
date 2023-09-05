from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

class ObtainTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                return Response({'token': token.key })  # Use 'token.key' to access the token key
        return Response(status=400)
