from rest_framework import serializers
from .models import users, Conversation, Message


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = users


class ConversationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Conversation


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message