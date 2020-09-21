from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return f"a {self.color} {self.name}"

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})


class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)


    def __str__(self):
        return f"{self.name} is a {self.breed} which {self.description} and is {self.age}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

class Feeding(models.Model):
  date = models.DateField('feeding date')
  meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[1][0])
  dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

  def __str__(self):
      return f"{self.get_meal_display()} on {self.date}"

  class Meta:
    ordering = ['-date']
