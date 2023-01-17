from rest_framework import serializers, exceptions

from mainapp.models import (
    Category, Product, Comment
)


class ProductSerializer(serializers.ModelSerializer):
    # category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category',
            'price', 'image', 'description',
            # 'category_name',
        )
        read_only_fields = (
            'category', 
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) # nested serializer
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'image',
            'products',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'product', 'user', 'comment_text',
            'raiting', 'created_at',
        )
        read_only_fields = (
            'created_at', 'user', 'product',
        )


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate_password(self, value):
        if len(value) < 8:
            raise exceptions.ValidationError('Password is too short')
        elif len(value) > 24:
            raise exceptions.ValidationError("Password is too long")
        return value


class AuthorizarionSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

