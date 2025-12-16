from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        permissions = [
            # (codename, human_readable_name)
            ("can_publish", "Can publish article"),
            ("can_unpublish", "Can unpublish article"),
            ("can_feature", "Can feature article on homepage"),
        ]