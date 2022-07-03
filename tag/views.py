from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from tag.models import Tag
from tag.serializers import TagSerializer


class TagsList(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Returns a list of Tags.', TagSerializer)},
                         operation_id='Get a list of Tags.',)
    def get(self, request, format=None):

        tags = Tag.objects.all().order_by("-pk")
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: openapi.Response('Returns a created Blog post.', TagSerializer), 400: "Invalid data."},
                         operation_id='Create a new Tag.', )
    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    @swagger_auto_schema(responses={200: openapi.Response('Returns details of a Tag.', TagSerializer), 404: "Tag not found."},
                         operation_id='Get details of a Tag.',)
    def get(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: openapi.Response('Returns details of an updated Tag.', TagSerializer), 404: "Tag not found.", 400: "Invalid data."},
                         operation_id='Update a Tag.',)
    def put(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)