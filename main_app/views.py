from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
from .forms import FeedingForm

# Create your views here.
def home(request):
    dogs = Dog.objects.all()
    return render(request, 'home.html', {'dogs': dogs})
    
def about(request):
    return render(request, 'about.html')

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  toys_dog_doesnt_have = Toy.objects.exclude(
      id__in=dog.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'dogs/detail.html', {
      'dog': dog, 'feeding_form': feeding_form,
      'toys': toys_dog_doesnt_have
  })


def assoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)
    
def add_feeding(request, dog_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)
    
class DogCreate(CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs/'

class DogUpdate(UpdateView):
  model = Dog
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'


class ToyList(ListView):
  model = Toy


class ToyDetail(DetailView):
  model = Toy


class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'


class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']


class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'
