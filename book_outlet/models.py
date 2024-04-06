from django.db import models
from django.core.validators import  MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Book(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(null=True,max_length=50)
  rating = models.IntegerField(null=True,
                               validators=[MinValueValidator(1), MaxValueValidator(5)])
  author = models.CharField(null=True, max_length=100)
  is_bestselling = models.BooleanField(default=False)
  slug = models.SlugField(default="", null=False, db_index= True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)
  def get_absolute_url(self):
    return reverse('book-detail', args=[self.slug])

  def __str__(self):
    return f"{self.id} {self.title} ({self.rating})"

