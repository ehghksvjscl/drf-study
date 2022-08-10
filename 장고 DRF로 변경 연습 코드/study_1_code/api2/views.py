from collections import OrderedDict
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from api2.serializers import CateTagSerializer, CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostSerializerDetail
from blog.models import Category, Post, Comment, Tag


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            "cateList":cateList,
            "tagList":tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('PageCnt', self.page.paginator.num_pages),
            ('CurPage', self.page.number),
        ]))


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'request': None,
                'format': self.format_kwarg,
                'view': self
    }

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }


        
    def retrieve(self, request, *args, **kwargs):
        
        def get_prev_next(instance):
            try:
                prev = instance.get_previous_by_update_dt()
            except instance.DoesNotExist:
                prev = None

            try:
                _next = instance.get_next_by_update_dt()
            except instance.DoesNotExist:
                _next = None

            return prev, _next 

        postInstance = self.get_object()
        prevInstance, nextInstance = get_prev_next(postInstance)
        commnetInstance = postInstance.comment_set.all()

        instance_data = {
            "post": postInstance,
            "prevPost": prevInstance,
            "nextPost": nextInstance,
            "commentList" : commnetInstance
        }
        serializer = PostSerializerDetail(instance=instance_data)
        return Response(serializer.data)

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer