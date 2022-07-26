from collections import OrderedDict

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import obj_to_post, prev_next_post, obj_to_comment
from api2.serializers import CommentSerializer, PostListSerializer, CateTagSerializer, PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }


# def get_prev_next(instance):
#     try:
#         prev = instance.get_previous_by_update_dt()
#     except instance.DoesNotExist:
#         prev = None
#
#     try:
#         next_ = instance.get_next_by_update_dt()
#     except instance.DoesNotExist:
#         next_ = None
#
#     return prev, next_


class PostRetrieveAPIView(RetrieveAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializerDetail

    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()

        postDict = obj_to_post(instance)
        prevDict, nextDict = prev_next_post(instance)
        commentDict = [obj_to_comment(c) for c in commentList]

        dataDict = {
            'post': postDict,
            'prevPost': prevDict,
            'nextPost': nextDict,
            'commentList': commentDict,
        }

        return Response(dataDict)


        # data = {
        #     'post': instance,
        #     'prevPost': prevInstance,
        #     'nextPost': nextInstance,
        #     'commentList': commentList,
        # }
        # serializer = self.get_serializer(instance=data)
        # return Response(serializer.data)

    # def get_serializer_context(self):
    #     return {
    #         'request': None,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }
