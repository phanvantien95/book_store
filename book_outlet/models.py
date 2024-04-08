from django.db import models
from django.core.validators import  MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Country(models.Model):
  name = models.CharField(max_length=50)
  code = models.CharField(max_length=2, unique=True)

  class Meta:
    verbose_name_plural = 'Country'
  def __str__(self):
    return f'{self.name} {self.code}'
class Address(models.Model):
  street = models.CharField(max_length=80)
  postal_code = models.CharField(max_length=6)
  city = models.CharField(max_length=50)
  def full_address(self):
    return f"{self.street} {self.city} {self.postal_code}"

  def __str__(self):
    return self.full_address()

  class Meta:
    verbose_name_plural = "Address"

class Author(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  address = models.OneToOneField(Address, null= True, on_delete=models.CASCADE)
  def full_name(self):
    return f"{self.first_name} {self.last_name}"
  def __str__(self):
    return self.full_name()

class Book(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(null=True,max_length=50)
  rating = models.IntegerField(null=True,
                               validators=[MinValueValidator(1), MaxValueValidator(5)])
  author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
  is_bestselling = models.BooleanField(default=False)
  slug = models.SlugField(default="", null=False, db_index= True)
  published_countries = models.ManyToManyField(Country, blank=True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)
  def get_absolute_url(self):
    return reverse('book-detail', args=[self.slug])

  def __str__(self):
    return f"{self.id} {self.title} ({self.rating})"

