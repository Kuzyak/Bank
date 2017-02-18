from django.shortcuts import render
from django.utils import timezone
from .models import Article
# Create your views here.
def index(request):
    firstbank = Article.objects.all()
    print ("!!!!!!!!!!!!!----!!!!!!!!!!!!!")
    num = len(firstbank)-1
    print (num)
    print ("!!!!!!!!!!!!!----!!!!!!!!!!!!!")
    return render(request, 'blogapp/index.html', {'firstbank':firstbank[num]})
