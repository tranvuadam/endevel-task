from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from tag.models import Tag
from tag.serializers import TagSerializer


class TagsList(APIView):
    @swagger_auto_schema(responses={200: openapi.Response('Returns list of tags.', TagSerializer)},
                         operation_id='Returns list of tags.',)
    def get(self, request, format=None):

        tags = Tag.objects.all().order_by("-pk")
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    @swagger_auto_schema(responses={200: openapi.Response('Returns details of a Tag.', TagSerializer), 404: "Tag not found."},
                         operation_id='Returns details of a Tag.',)
    def get(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)