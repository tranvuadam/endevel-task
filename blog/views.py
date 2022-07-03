from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer
from tag.models import Tag


class HomePageView(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Returns list of latest 3 Blog posts.', BlogPostSerializer)},
                         operation_id='Get a list of 3 latest blog posts.', )
    def get(self, request, format=None):
        blog_posts = BlogPost.objects.all().order_by("-pk")[:3]
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


tag_param = openapi.Parameter('tags', openapi.IN_QUERY, description="Filter blog posts by Tag ID.",
                              type=openapi.TYPE_INTEGER, )


class BlogPostList(APIView):
    @swagger_auto_schema(manual_parameters=[tag_param],
                         responses={200: openapi.Response('Get a list of blog posts(optional: filtered by Tags).', BlogPostSerializer),
                                    400: "Invalid tag ID format."},
                         operation_id='Returns list of blog posts.', )
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

    @swagger_auto_schema(responses={200: openapi.Response('Returns created Blog post.', BlogPostDetailSerializer), 400: "Invalid data."},
                         operation_id='Create new Blog post.', )
    def post(self, request, format=None):
        serializer = BlogPostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(BlogPost, pk=pk)

    @swagger_auto_schema(responses={200: openapi.Response('Returns details of a Blog post.', BlogPostDetailSerializer), 404: "Blog Post not found."},
                         operation_id='Get details of a Blog post.', )
    def get(self, request, pk, format=None):
        blog_post = self.get_object(pk)
        serializer = BlogPostDetailSerializer(blog_post)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: openapi.Response('Returns details of a updated Blog post.', BlogPostDetailSerializer), 404: "Blog Post not found.", 400: "Invalid data."},
                         operation_id='Update details of a Blog post.', )
    def put(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogPostDetailSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostAddTag(APIView):
    def get_object(self, pk):
        return get_object_or_404(BlogPost, pk=pk)

    def get_tag_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    @swagger_auto_schema(responses={200: openapi.Response("Returns a Blog post with an added Tag", BlogPostDetailSerializer), 404: "Blog Post or Tag not found."},
                         operation_id='Add Tag to a Blog post.', )
    def put(self, request, pk, tag_pk, format=None):
        blog = self.get_object(pk)
        tag = self.get_tag_object(tag_pk)

        blog.tags.add(tag)
        serializer = BlogPostDetailSerializer(blog)
        return Response(serializer.data)
