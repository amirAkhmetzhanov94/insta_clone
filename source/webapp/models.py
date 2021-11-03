from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    picture = models.ImageField(blank=False, upload_to="posts", verbose_name="Picture")

    description = models.TextField(max_length=3000, blank=True, null=True, default=None, verbose_name="Description")

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1, verbose_name="Author")

    created_on = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(get_user_model(), related_name="blog_post")

    def __str__(self):
        return f"{self.pk} - {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post", related_name="comments")

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
                               verbose_name="Author of comment")

    text = models.TextField(max_length=100, verbose_name="comment")

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:20]
