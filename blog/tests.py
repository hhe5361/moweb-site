from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class BlogViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test-password",
        )

    def test_post_list_shows_published_posts(self):
        Post.objects.create(
            author=self.user,
            title="Published post",
            text="Visible text",
            published_date=timezone.now(),
        )
        Post.objects.create(
            author=self.user,
            title="Draft post",
            text="Hidden text",
        )

        response = self.client.get(reverse("post_list"))

        self.assertContains(response, "Published post")
        self.assertNotContains(response, "Draft post")

    def test_post_detail_shows_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Detail post",
            text="Detail text",
            published_date=timezone.now(),
        )

        response = self.client.get(reverse("post_detail", kwargs={"pk": post.pk}))

        self.assertContains(response, "Detail post")
        self.assertContains(response, "Detail text")

    def test_post_list_shows_post_image_when_available(self):
        Post.objects.create(
            author=self.user,
            title="Image post",
            text="Image text",
            image="images/test.png",
            published_date=timezone.now(),
        )

        response = self.client.get(reverse("post_list"))

        self.assertContains(response, 'src="/media/images/test.png"')
        self.assertContains(response, 'alt="Image post"')

    def test_logged_in_user_can_create_post(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("post_new"),
            {"title": "New post", "text": "New text"},
        )

        post = Post.objects.get(title="New post")
        self.assertRedirects(response, reverse("post_detail", kwargs={"pk": post.pk}))
