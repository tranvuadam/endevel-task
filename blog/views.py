from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer


class HomePageView(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Returns list of latest 3 blog posts.', BlogPostSerializer)},
                         operation_id='List of 3 latest blog posts.',)
    def get(self, request, format=None):
        blog_posts = BlogPost.objects.all().order_by("-pk")[:3]
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


tag_param = openapi.Parameter('tags', openapi.IN_QUERY, description="Filter blog posts by tag ID.", type=openapi.TYPE_INTEGER,)


class BlogPostList(APIView):
    @swagger_auto_schema(manual_parameters=[tag_param],
                         responses={200: openapi.Response('Returns list of blog posts.', BlogPostSerializer), 400: "Invalid tag ID format."},
                         operation_id='Returns list of blog posts.',)
    def get(self, request, format=None):
        if 'tags' in self.request.query_params:
            # also works with multiple tags by chaining, example: ?tags=1&tags=2
            tags = self.request.query_params.getlist('tags', None)
            try:
                blog_posts = BlogPost.objects.filter(tags__in=tags).distinct().order_by("-pk")
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            blog_posts = BlogPost.objects.all().order_by("-pk")
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


blog_detail_response = openapi.Response('Returns details of a Blog post.', BlogPostDetailSerializer)


class BlogPostDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(BlogPost, pk=pk)

    @swagger_auto_schema(responses={200: blog_detail_response, 404: "Blog Post not found."},
                         operation_id='Returns details of a Blog post.',)
    def get(self, request, pk, format=None):
        blog_post = self.get_object(pk)
        serializer = BlogPostDetailSerializer(blog_post)
        return Response(serializer.data)


