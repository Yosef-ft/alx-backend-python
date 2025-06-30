from rest_framework import serializers
from .models import users, Conversation, Message
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email

class UsersSerializer(serializers.ModelSerializer):

	full_name = serializers.SerializerMethodField()

	class Meta:
		model = users
		fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'password', 'username']

		extra_kwargs = {
			'password' : {'write_only': True},
			'email' : {'required': True},
			'username': {'required': True}
		}

	
	def get_full_name(self, obj):
		return f"{obj.first_name} {obj.last_name}"
	
	def validate_password(self, value):

		if len(value) < 8:
			raise serializers.ValidationError("Password must be at least 8 chars long")
		return value
	
	def validate_email(self, value):
		try:
			validate_email(value)
		except ValidationError:
			raise serializers.ValidationError("Invalid email format")

		if users.objects.filter(email=value).exists():
			raise serializers.ValidationError("Email already exists")
		return value

	def validate_username(self, value):

		if users.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists")
		return value
		

	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data['password'])
		return super().create(validated_data=validated_data)


class ConversationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Conversation
		# serializers.CharField
		fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = "__all__"



class MessageSendSerializer(serializers.Serializer):
	message_body = serializers.CharField()

	def create(self, validated_data):
		return Message.objects.create(**validated_data)
