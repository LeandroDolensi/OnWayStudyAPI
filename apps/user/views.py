from rest_framework.viewsets import ModelViewSet
from apps.user.models import User
from apps.user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "nickname"
