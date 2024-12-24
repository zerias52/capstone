from django.shortcuts import render

"""
Class-based views:

View        = generic view
ListView    = get a list of records
DetailView  = get a single(detail) record
CreateView  = create a new record
DeleteView  = remove a record
UpdateView  = modify an existing record
LoginView   = login
"""

# Create your views here.
def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")
