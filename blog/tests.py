from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer
from tag.models import Tag


class BlogPostTest(APITestCase):
    def setUp(self):
        tag = Tag.objects.create(name="tag")
        tag2 = Tag.objects.create(name="tag2")
        tag3 = Tag.objects.create(name="tag3")

        blog = BlogPost.objects.create(title="blog_title", detail="blog_detail", text="blog_text")
        blog.tags.add(tag, tag2)
        blog2 = BlogPost.objects.create(title="blog_title2", detail="blog_detail2", text="blog_text2")
        blog2.tags.add(tag2, tag3)
        blog3 = BlogPost.objects.create(title="blog_title3", detail="blog_detail3", text="blog_text3")
        blog3.tags.add(tag)
        blog4 = BlogPost.objects.create(title="blog_title4", detail="blog_detail4", text="blog_text4")
        blog4.tags.add(tag, tag3)

    def test_home_page_list(self):
        url = reverse('home_page')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0], BlogPostSerializer(BlogPost.objects.get(pk=4)).data)
        self.assertEqual(response.data[1], BlogPostSerializer(BlogPost.objects.get(pk=3)).data)
        self.assertEqual(response.data[2], BlogPostSerializer(BlogPost.objects.get(pk=2)).data)

    def test_new_blog_post(self):
        url = reverse('blog:blog_post_list')
        data = {'title': "blog_title", "detail": "blog_detail", "text": "blog_text", "tags": [1, 2]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data, BlogPostDetailSerializer(BlogPost.objects.get(pk=5)).data)

    def test_new_blog_post_invalid_data(self):
        url = reverse('blog:blog_post_list')
        data = {'invalid_field': "blog_title", "detail": "blog_detail", "text": "blog_text", "tags": [1, 2]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blog_post_detail(self):
        url = reverse('blog:blog_post_detail', kwargs={'pk': 4})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # num of fields
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data, BlogPostDetailSerializer(BlogPost.objects.get(pk=4)).data)

    def test_blog_post_detail_not_found(self):
        url = reverse('blog:blog_post_detail', kwargs={'pk': 5})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_post_detail_put(self):
        url = reverse('blog:blog_post_detail', kwargs={'pk': 4})
        data = {'title': "blog_title", "detail": "blog_detail", "text": "blog_text", "tags": [2]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # num of fields
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data, BlogPostDetailSerializer(BlogPost.objects.get(pk=4)).data)

    def test_blog_post_detail_put_invalid_data(self):
        url = reverse('blog:blog_post_detail', kwargs={'pk': 4})
        data = {'invalid_data': "blog_title", "detail": "blog_detail", "text": "blog_text", "tags": [2]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blog_post_detail_add_tag(self):
        tag_id = 2
        url = reverse('blog:blog_post_add_tag', kwargs={'pk': 4, 'tag_pk': tag_id})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # num of fields
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data, BlogPostDetailSerializer(BlogPost.objects.get(pk=4)).data)
        self.assertIn(tag_id, BlogPostDetailSerializer(BlogPost.objects.get(pk=4)).data['tags'])

    def test_blog_post_detail_add_tag_not_found_tag(self):
        url = reverse('blog:blog_post_add_tag', kwargs={'pk': 4, 'tag_pk': 42})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_post_detail_add_tag_not_found_blog(self):
        url = reverse('blog:blog_post_add_tag', kwargs={'pk': 42, 'tag_pk': 2})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_post_list_no_tags(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0], BlogPostSerializer(BlogPost.objects.get(pk=4)).data)
        self.assertEqual(response.data[1], BlogPostSerializer(BlogPost.objects.get(pk=3)).data)
        self.assertEqual(response.data[2], BlogPostSerializer(BlogPost.objects.get(pk=2)).data)
        self.assertEqual(response.data[3], BlogPostSerializer(BlogPost.objects.get(pk=1)).data)

    def test_blog_post_list_valid_tag(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=2", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0], BlogPostSerializer(BlogPost.objects.get(pk=2)).data)
        self.assertEqual(response.data[1], BlogPostSerializer(BlogPost.objects.get(pk=1)).data)

    def test_blog_post_list_valid_tags(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=2&tags=3&", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0], BlogPostSerializer(BlogPost.objects.get(pk=4)).data)
        self.assertEqual(response.data[1], BlogPostSerializer(BlogPost.objects.get(pk=2)).data)
        self.assertEqual(response.data[2], BlogPostSerializer(BlogPost.objects.get(pk=1)).data)

    def test_blog_post_list_one_tag_not_found_ignored(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=2&tags=3&tags=404", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0], BlogPostSerializer(BlogPost.objects.get(pk=4)).data)
        self.assertEqual(response.data[1], BlogPostSerializer(BlogPost.objects.get(pk=2)).data)
        self.assertEqual(response.data[2], BlogPostSerializer(BlogPost.objects.get(pk=1)).data)

    def test_blog_post_list_tag_not_found(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=404", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_blog_post_list_tags_not_found(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=404&tags=405", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_blog_post_list_invalid_tag(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=invalid_tag", format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blog_post_list_invalid_tags(self):
        url = reverse('blog:blog_post_list')
        response = self.client.get(url + "?tags=1&tags=invalid_tag", format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
