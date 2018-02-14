from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse

from postings.models import BlogPost


User = get_user_model()
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user = User(username='testcase', email='testcase@testcase.com')
        user.set_password('testcasepassword')
        user.save()

        BlogPost.objects.create(user=user, title='Test Post', content='Random content')

    def test_single_user(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)

    def test_single_post(self):
        counter = BlogPost.objects.count()
        self.assertEqual(counter, 1)
    
    def test_get_list(self):
        # test the get list
        data = {}
        url = api_reverse("postings:post-list-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item(self):
        # test the get list
        data = {"title": "Some rando title", "content": "some more content"}
        url = api_reverse("postings:post-list-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_item(self):
        # test the get list
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        # test the get list
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_item_with_user(self):
        # test the get list
        blog_post = BlogPost.objects.first()
        #print(blog_post.content)
        url = blog_post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_post_item_with_user(self):
        # test the get list
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {"title": "Some rando title", "content": "some more content"}
        url = api_reverse("postings:post-list-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_ownership(self):
        # test the get list
        owner = User.objects.create(username='testuser22222')
        blog_post = BlogPost.objects.create(
                user=owner, 
                title='New title', 
                content='some_random_content'
                )

        user_obj            = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload             = payload_handler(user_obj)
        token_rsp           = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = blog_post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
