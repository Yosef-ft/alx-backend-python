
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        
        return False           