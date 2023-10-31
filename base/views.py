from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main(request):
    return HttpResponse("Dieser Text wurde geändert.")

def EPSMarcel(request):
    return render(request, "base/LP_marcel.html")