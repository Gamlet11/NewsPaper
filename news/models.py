from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles_rate = Post.objects.filter(author_id=self.pk).aggregate(sum_articles=Sum('news_rate'))['news_rate'] * 3
        comments_rate = Comment.objects.filter(users_id=self.users).aggregate(sum_articles=Sum('comment_rate'))['comment_rate']
        comments_articles_rate = Comment.objects.filter(post__author__users=self.users).aggregate(sum_posts=Sum('comment_rate'))['comment_rate']
        self.rating = articles_rate + comments_rate + comments_articles_rate
        self.save()


sport = 'SP'
education = 'ED'
policy = 'PO'
economy = 'EC'

TOPICS = [
    (sport, 'Спорт'),
    (education, 'Образование'),
    (policy, 'Политика'),
    (economy, 'Экономика')
]


class Category(models.Model):
    topics = models.CharField(max_length=2, choices=TOPICS, default=economy, unique=True)


news = 'NE'
articles = 'AR'

TYPES = [
    (news, 'Новости'),
    (articles, 'Статьи')
]


class Post(models.Model):
    choice_types = models.CharField(max_length=2, choices=TYPES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')
    news_title = models.CharField(max_length=255)
    news_text = models.TextField()
    news_rate = models.IntegerField(default=0)

    def preview(self):
        dots = self.news_text
        return dots[0:124] + '...'

    def like(self):
        self.news_rate += 1
        self.save()

    def dislike(self):
        self.news_rate -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()
