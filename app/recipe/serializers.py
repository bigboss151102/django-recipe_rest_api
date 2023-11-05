"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        """
        Dòng này loại bỏ trường "tags" khỏi dữ liệu đã xác nhận và lưu vào biến tags.
        """
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            """
            Dòng này thực hiện việc tìm kiếm hoặc tạo mới một đối tượng "Tag."
            Nếu tag đã tồn tại với thông tin như đã cung cấp (dựa trên người dùng và thông tin tag),nó sẽ được tìm kiếm.
            Nếu không tồn tại, nó sẽ được tạo mới.
            """
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            """
            Thêm đối tượng "tag_obj" vào trường "tags" của đối tượng recipe.
            """
            recipe.tags.add(tag_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
