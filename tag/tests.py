from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from tag.models import Tag
from tag.serializers import TagSerializer


class TagTest(APITestCase):
    def setUp(self):
        Tag.objects.create(name="tag")
        Tag.objects.create(name="tag2")
        Tag.objects.create(name="tag3")

    def test_tag_list(self):
        url = reverse('tag:tag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0], TagSerializer(Tag.objects.get(pk=3)).data)
        self.assertEqual(response.data[1], TagSerializer(Tag.objects.get(pk=2)).data)
        self.assertEqual(response.data[2], TagSerializer(Tag.objects.get(pk=1)).data)

    def test_tag_detail(self):
        url = reverse('tag:tag_detail', kwargs={'pk': 3})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # num of fields
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, TagSerializer(Tag.objects.get(pk=3)).data)

    def test_tag_detail_not_found(self):
        url = reverse('tag:tag_detail', kwargs={'pk': 4})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)