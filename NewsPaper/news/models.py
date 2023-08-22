from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_rating = models.IntegerField(default = 0)
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = Post.objects.filter(author__user_auth = self.user_auth).values('post_rating')
        post_rating_sum = 0
        if post_rating is not None:
            for i in post_rating:
                post_rating_sum = post_rating_sum + i['post_rating']
        post_rating_sum *= 3

        comment_rating = Comment.objects.filter(user = self.user_auth).values('comment_rating')
        comment_rating_sum = 0
        if comment_rating is not None:
            for i in comment_rating:
                comment_rating_sum = comment_rating_sum + i['comment_rating']

        comment_rating_posts = Comment.objects.filter(post__author__user_auth = self.user_auth).values('comment_rating')
        comment_rating_posts_sum = 0
        if comment_rating_posts is not None:
            for i in comment_rating_posts:
                comment_rating_posts_sum = comment_rating_posts_sum + i['comment_rating']
        self.user_rating = post_rating_sum + comment_rating_sum + comment_rating_posts_sum
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length = 25, unique = True)


class Post(models.Model):
    post_select = models.BooleanField(default = False)
    post_dt = models.DateTimeField(auto_now_add = True)
    post_tittle = models.CharField(max_length = 60)
    post_text = models.TextField()
    post_rating = models.IntegerField(default = 0)

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    category = models.ManyToManyField(Category, through = 'PostCategory')

    def like_p(self):
        self.post_rating = self.post_rating + 1
        self.save()

    def dislike_p(self):
        self.post_rating = self.post_rating - 1
        self.save()

    def preview(self):
        if len(self.post_text) <= 124:
            return self.post_text + "..."
        else:
            return self.post_text[:124] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_dt = models.DateTimeField(auto_now_add = True)
    comment_rating = models.IntegerField(default = 0)

    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def like_c(self):
        self.comment_rating = self.comment_rating + 1
        self.save()

    def dislike_c(self):
        self.comment_rating = self.comment_rating - 1
        self.save()


