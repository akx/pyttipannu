from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class RecipeSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Recipe


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.public()
    serializer_class = RecipeSerializer


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
