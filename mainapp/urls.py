from django.urls import path
from rest_framework.routers import DefaultRouter as DR

from mainapp.views import (
    CategoryView, 
    ProductView,
    CommentView,
    RegistrationView,
    AuthorizarionView,
)

router = DR()

router.register('categories', CategoryView, basename='category')
router.register('products', ProductView, basename='product')
router.register('comments', CommentView, basename='comment')

urlpatterns = [
    path('reg/', RegistrationView.as_view()),
    path('login/', AuthorizarionView.as_view()),
]

urlpatterns += router.urls


# {
#     "username": "LeVaSiK001",
#     "email": "lev201611@gmail.com",
#     "password": "147258qaz!"
# }