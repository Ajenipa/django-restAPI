from urllib import request
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from .models import Article
from django.http import HttpResponse,JsonResponse
from .sterilize import ModelArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here.
#class based api view begins

class ArticleApiView(APIView):

    def get(self,request):
        article = Article.objects.all()
        serialize = ModelArticleSerializer(article, many=True)
        return Response(serialize.data)
    def post(self,request):
        serialize =ModelArticleSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class ArticleApiDetailView(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,id):
        article = self.get_object(id)
        serialize = ModelArticleSerializer(article)
        return Response(serialize.data)
    def put(self,request,id):
        article = self.get_object(id)
        serialize = ModelArticleSerializer(article, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)  
# class view api ends
#function view begins
#@csrf_exempt  this is used whenever you are not using the api_view
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        article = Article.objects.all()
        serialize = ModelArticleSerializer(article, many=True)
        #return JsonResponse(serialize.data, safe=False) , this is used whenever you are not using the api_view
        return Response(serialize.data)
    elif request.method == "POST":
        #data = JSONParser().parse(request)  , this is used whenever you are not using the api_view
        serialize = ModelArticleSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
            #return JsonResponse(serialize.data, status=200) , this is used whenever you are not using the api_view
        return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)
#@csrf_exempt , this is used whenever you are not using the api_view
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)     
    except Article.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        #return HttpResponse(status=404)    , this is used whenever you are not using the api_view
    if request.method == "GET":
        serialize = ModelArticleSerializer(article)
        return Response(serialize.data)
    elif request.method == "PUT":
        #data = JSONParser().parse(request)  , this is used whenever you are not using the api_view
        serialize = ModelArticleSerializer(article,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)
    else :
        if request.method == "DELETE":
            article.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

#function view api ends
#genericview mixin begins
class GenericApiView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = ModelArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "id"
    authentication_classes = [TokenAuthentication]
    #authentication_classes = [BasicAuthentication,SessionAuthentication] 'used for basic and session authentication
    permission_classes = [IsAuthenticated]
    def get(self,request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self,request):
        return self.create(request)
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id=None):
        return self.destroy(request,id)
# viewset

class ArticleViewSet(viewsets.ViewSet):
    def list(self,request):
        article = Article.objects.all()
        serialize = ModelArticleSerializer(article, many=True)
        return Response(serialize.data)
    def create(self,request):
        serialize = ModelArticleSerializer(data = request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serialize = ModelArticleSerializer(article)
        return Response(serialize.data)
    def update(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        serialize = ModelArticleSerializer(article, request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status = status.HTTP_100_CONTINUE)
        return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)
