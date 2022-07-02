from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer


class HomePageView(APIView):

    def get(self, request, format=None):
        blog_posts = BlogPost.objects.all().order_by("-pk")[:3]
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


class BlogPostList(APIView):

    def get(self, request, format=None):
        if 'tags' in self.request.query_params:
            tags = self.request.query_params.getlist('tags', None)
            try:
                blog_posts = BlogPost.objects.filter(tags__in=tags).distinct().order_by("-pk")
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            blog_posts = BlogPost.objects.all().order_by("-pk")
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


class BlogPostDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(BlogPost, pk=pk)

    def get(self, request, pk, format=None):
        blog_post = self.get_object(pk)
        serializer = BlogPostDetailSerializer(blog_post)
        return Response(serializer.data)


