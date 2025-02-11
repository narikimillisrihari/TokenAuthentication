from django.urls import path
from .views import LoginView,ProtectedView,RegisterView,ListCreateMovieAPIView,RetrieveUpdateDestoryMovieAPIView,UserMovieSerializerAPIView



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('register/', RegisterView.as_view(), name='register'),
    path('listcreatemovie/',ListCreateMovieAPIView.as_view(),name='get_post_movies'),
    path('retrievemovie/<int:pk>',RetrieveUpdateDestoryMovieAPIView.as_view(),name='get_delete_update_movie'),
    path('usermoviedeatils/<int:pk>/',UserMovieSerializerAPIView.as_view(),name='get_user_movie_deatils'),
    
]