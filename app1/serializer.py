from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User  # Use your custom User model if applicable
from app1.models import Movie


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # Remove 'password2' as it's not needed for creating the user
        validated_data.pop('password2')

        # Create and return the user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class MovieSerializer(serializers.ModelSerializer):
    creator=serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model=Movie
        fields=('id','title','year','creator','created_at','updated_at')

class UserMovieSerializer(serializers.ModelSerializer):
    movies=serializers.PrimaryKeyRelatedField(many=True,queryset=Movie.objects.all())
    # movies=MovieSerializer(many=True,read_only=True)
    class Meta:
        model=User
        fields=('id','username','movies')
