"""restproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import article_list,article_detail,ArticleApiView,ArticleApiDetailView,GenericApiView,ArticleViewSet,ArticleGenericViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register('article',ArticleViewSet,basename='article')
router.register('article',ArticleGenericViewSet,basename='article') # FOR THE ARTICLE GENERIC VIEWSET
urlpatterns = [
    #path('article/',article_list, name="article-list"),
    path('article/',ArticleApiView.as_view(), name="article-list"),
    #path('article/<int:pk>/',article_detail, name="article-detail"),
    path('article/<int:id>/',ArticleApiDetailView.as_view(), name="article-detail"),
    path('generic/article/',GenericApiView.as_view(), name="article-list"),
    path('generic/article/<int:id>/',GenericApiView.as_view(), name="article-detail"),
    path('viewset/',include(router.urls)),
    #path('viewset/<int:id>/',include(router.urls)),
    path('genericviewset/',include(router.urls)),
    

]
