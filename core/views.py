from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.
# views.py
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"https://recipe-sharing-drf.onrender.com/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

# class UserLogoutView(APIView):
#     # def get(self, request):
#     #     if request.user.is_authenticated:
#     #         request.user.auth_token.delete()
#     #         logout(request)
#     #         return redirect('login')  # Return a redirect response
#     #     return Response(status=status.HTTP_400_BAD_REQUEST)  # Or any appropriate response for non-authenticated user

#     def post(self, request):  # Add this method to handle POST requests
#         if request.user.is_authenticated:
#             request.user.auth_token.delete()
#             logout(request)
#             return redirect('login')  # Return a redirect response
#         return Response(status=status.HTTP_400_BAD_REQUEST)  # Or any appropriate response for non-authenticated user

# class UserLogoutAPIView(APIView):
#     def post(self, request):
#         try:
#             # Get the user's token from the request headers
#             token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
#             token = Token.objects.get(key=token_key)
#             # Delete the token
#             token.delete()
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#         except AttributeError:
#             return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutAPIView(APIView):
#     def post(self, request):
#         try:
#             auth_header = request.META.get('HTTP_AUTHORIZATION')
#             if not auth_header:
#                 return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
#             token_key = auth_header.split(' ')[1]
#             token = Token.objects.get(key=token_key)
#             token.delete()
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#         except AttributeError:
#             return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
# class UserLogoutAPIView(APIView):
#     def get(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#          # return redirect('login')
#         return Response({'success' : "logout successful"})
    
class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Delete the token associated with the user
            request.user.auth_token.delete()
            
            # Logout the user
            logout(request)
            return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': 'Token not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
