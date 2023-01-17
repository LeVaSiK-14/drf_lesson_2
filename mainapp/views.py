from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from mainapp.serializers import (
    CategorySerializer,
    ProductSerializer,
    CommentSerializer,
    RegistrationSerializer,
    AuthorizarionSerializer,
)
from mainapp.models import (
    Category, Product, Comment,
)
# ovlbwwrhznxlyunp

from mainapp.send_gmail import send_msg

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework import permissions
from rest_framework.decorators import action


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['post'], detail=True, serializer_class=ProductSerializer)
    def add_products(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product = Product.objects.create(
            category=category,
            name=data.get('name'),
            price=data.get('price'),
            image=data.get('image'),
            description=data.get('description')
        )
        return Response(ProductSerializer(product).data)


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_fields = (
        'name', 'category__name',
    )
    search_fields = (
        'name', 'category__name',
    )
    ordering_fields = (
        'price', 'id',
    )



    @action(methods=['post', ], detail=True, serializer_class=CommentSerializer, permission_classes = (permissions.IsAuthenticatedOrReadOnly, ))
    def add_comment(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)# get http data > json data
        # serializer = {
        #     'raiting': 3,
        #     'comment_text': 'text'
        # }
        serializer.is_valid(raise_exception=True)
        comment = Comment.objects.create(
            user=request.user,
            product=self.get_object(),
            raiting=serializer.validated_data.get('raiting'),
            comment_text=serializer.validated_data.get('comment_text')
        )
        # comment type(python object)
        return Response(CommentSerializer(comment).data) # python object > json object


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"message": 'User with such username is already exists'})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        send_msg(email=email, username=username)

        token = Token.objects.create(user=user)

        return Response({"token": token.key})


class AuthorizarionView(APIView):
    def post(self, request):
        serializer = AuthorizarionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            if check_password(password, user.password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": 'Password is not valid'}, status=400)
        return Response({'error': 'this username is not registered'}, status=400)

