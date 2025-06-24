from django.shortcuts import render, get_list_or_404
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UsersSerializer


class ConversationViewSet(ViewSet):
	queryset = Conversation.objects.all()

	def list(self, request):
		serializer = ConversationSerializer(self.queryset, many=True)
		return Response(serializer.data)
	

	def create(self, request, *args, **kwargs):
		serializer = ConversationSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MessageViewSet(ViewSet):
	queryset = Message.objects.all()


	def list(self, request):
		serializer =  MessageSerializer(self.queryset, many=True)
		return Response(serializer.data)
	

	@action(detail=False, methods=['post'])
	def send_message(self, request):
		serializer = MessageSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(sender=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)