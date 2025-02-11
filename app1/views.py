import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User  # Use a custom User model if needed
from app1.serializer import RegisterSerializer, UserSerializer ,MovieSerializer,UserMovieSerializer # Assuming these serializers exist
from django.conf import settings 
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from app1.models import Movie
from .permission import IsOwnerOrReadOnly


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected endpoint!"})
    
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and generate JWT tokens
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]  #  Allow anyone to access the login endpoint

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self, request):
        self.permission_classes = [IsAuthenticated]  # Only authenticated users can access
        self.check_permissions(request)

        ALLOWED_USER_ID = 1  # Change this to the specific user ID you want to allow

        def get(self, request):
            self.permission_classes = [IsAuthenticated]  # Only authenticated users can access
            self.check_permissions(request)

        ALLOWED_USER_ID = 1  # Change this to the specific user ID who can see all users

        if request.user.id == ALLOWED_USER_ID:
            # If the allowed user is accessing, show all registered users (without passwords)
            users = User.objects.all()
            user_data = [{"id": user.id, "username": user.username} for user in users]
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            # Other users can only see their own data
            return Response({"error": "You do not have permission to access this data."}, status=status.HTTP_403_FORBIDDEN)
# class LoginView(APIView):
#     print("it was loign view")    
#     def post(self, request):
#         print("it was post request")
#         # Get username and password from the request data
#         username = request.data.get("username")
#         password = request.data.get("password")
#         # Authenticate the user with the provided credentials
#         user = authenticate(username=username, password=password)
        
#         if user:
#             # Now, after the user is authenticated, we can request the access token using the TokenObtainPairView
#             # We will manually create the request to the TokenObtainPairView
            
#             # Send a request to the token obtain endpoint to get access and refresh tokens
#             token_request_data = {
#                 "username": username,
#                 "password": password,
#             }
            
#             token_response = self.obtain_token(token_request_data)
#             print(token_response)
            
#             if token_response.get("access"):
#                 # Return the tokens in the response
#                 return Response({
#                     "access": token_response["access"],
#                     "refresh": token_response["refresh"]
#                 })
#             else:
#                 return Response({"error": "Token generation failed."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#     def obtain_token(self, data):
#         """
#         Helper method to obtain the JWT tokens using TokenObtainPairView logic.
#         """
#         # Send a POST request to the TokenObtainPairView
#         response = requests.post('http://127.0.0.1:8000/api/v1/auth/token/', data=data)
#         return response.json()
    
#     def get(self, request):
#         self.permission_classes = [IsAuthenticated]  # Only authenticated users can access
#         self.check_permissions(request)

#         ALLOWED_USER_ID = 1  # Change this to the specific user ID you want to allow

#         if request.user.id == ALLOWED_USER_ID:
#             # If the allowed user is accessing, show all registered users (without passwords)
#             users = User.objects.all()
#             user_data = [{"id": user.id, "username": user.username} for user in users]
#             return Response(user_data, status=status.HTTP_200_OK)
#         else:
#             # Other users can only see their own data
#             return Response({"error": "You do not have permission to access this data."}, status=status.HTTP_403_FORBIDDEN)
        
class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class=MovieSerializer
    queryset=Movie.objects.all()
    permission_classes=[IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(creator=self.request.user)

class RetrieveUpdateDestoryMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=MovieSerializer
    queryset=Movie.objects.all()
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]

class UserMovieSerializerAPIView(RetrieveAPIView):
    serializer_class=UserMovieSerializer
    queryset=User.objects.all()

