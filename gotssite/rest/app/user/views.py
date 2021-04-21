from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest.app.user.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest.app.user.models import User

import base64

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status_code' : status.HTTP_200_OK,
            'message': 'User registered  successfully',
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class UserLoginView(APIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_header = request.META['HTTP_AUTHORIZATION']
            encoded_credentials = auth_header.split(' ')[1]
            email, password = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
            data = {
                'email': email.lower(),
                'password': password,
            }
            try:
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                response = {
                    'success' : 'True',
                    'status_code' : status.HTTP_200_OK,
                    'message': 'User logged in successfully',
                    'user': {
                        'email': serializer.data['email'],
                        'username': serializer.data['username'],
                    },
                    'token' : serializer.data['token'],
                }
                status_code = status.HTTP_200_OK
            except Exception as e:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'false',
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User does not exists',
                    'error': str(e)
                }
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad requast',
                'error': 'Bad requast'
            }
        return Response(response, status=status_code)

class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user_profile = User.objects.get(email=request.user.email.lower())
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'username': user_profile.username,
                    'email': user_profile.email,
                    'country': user_profile.country,
                }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)