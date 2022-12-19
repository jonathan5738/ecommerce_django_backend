from django.shortcuts import render
from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from . serializes import UserSerializer, LoginSerializer



class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = {key: value for(key, value) in UserSerializer(user).data.items() }
            token = Token.objects.create(user=user)
            response['token'] = token.key
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username, password = serializer.data.values()
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            token = Token.objects.get(user=user)
            if not token and user:
                # in case the current token expired and the user is found create a new token
                # for that user
                token = Token.objects.create(user=user)
            return Response({'id': user.pk, 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageUserAccountView(APIView):
    authentication_classes = [TokenAuthentication]
    def patch(self, request, *args, **kwargs):
        user = request.user
        allowedFields = ['username', 'first_name', 'last_name', 'email']
        receivedFields = request.data.keys()
        isValid = True
        for key in receivedFields:
            if not key in allowedFields:
                isValid = False; break
        
        if not isValid or len(receivedFields) == 0:
            return Response({'error': 'invalid field sent'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            if not token and user:
                # in case the current token expired and the user is found create a new token
                # for that user
                token = Token.objects.create(user=user)
            return Response({'id': user.pk, 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pass


