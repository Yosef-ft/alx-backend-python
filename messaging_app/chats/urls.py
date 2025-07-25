from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from .auth import RegisterView

router = routers.DefaultRouter()


router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('register/', RegisterView.as_view(), name="Register")
]