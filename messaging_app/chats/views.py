from django.shortcuts import render, get_list_or_404
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageSendSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter

class ConversationViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, IsParticipantOfConversation]
	queryset = Conversation.objects.all()
	serializer_class = ConversationSerializer
	filter_backends = [DjangoFilterBackend, filters.SearchFilter]
	filterset_fields = ['participants']
	search_fields = ['participants__email'] 

	def get_queryset(self):
		user = self.request.user
		return Conversation.objects.filter(participants=user)



class MessageViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, IsParticipantOfConversation]
	queryset = Message.objects.all()
	filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
	filterset_class = MessageFilter
	search_fields = ['message_body']
	serializer_class = MessageSendSerializer


	@action(detail=False, methods=['post'])
	def send_message(self, request, conversation_pk):
		try:
			conversation = Conversation.objects.get(pk=conversation_pk)
		except Conversation.DoesNotExist:
			return Response(
				{"detail" : "Conversation not found"},
				status=status.HTTP_400_BAD_REQUEST				
			)

		if not conversation.participants.filter(pk=request.user.pk).exists():
			return Response(
                {"detail": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN					
			)
		
		serializer = self.get_serializer(data=request.data)		
		if serializer.is_valid(raise_exception=True):
			serializer.save(
				sender = request.user,
				conversation=conversation
			)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)			
	