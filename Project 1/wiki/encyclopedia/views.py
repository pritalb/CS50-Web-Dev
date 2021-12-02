from django.shortcuts import render
from django.http import HttpResponse
from . import util
from markdown2 import markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {"entry": markdown(util.get_entry(title)), "title": title, })
    else:
        return render(request, "encyclopedia/entry.html", {"entry": "No entry with the title {title} exists." })

def search(request):
    query = request.GET.get('q')

    return entry(request, query)

def create(request):
    entry_list = util.list_entries()
    title = request.POST.get('title')
    description = request.POST.get('description')

    if request.method == "POST":
        # if 'title' in request.POST and 'description' in request.POST:

        if not title in entry_list:
            util.save_entry(title, description)
            return render(request, "encyclopedia/create.html", { "error": f"Entry about {title} created."})
        else:
            return render(request, "encyclopedia/create.html", { "error": f"{title} already exists."})
       # return render(request, "encyclopedia/create.html", { "error": ""})
    return render(request, "encyclopedia/create.html")

def edit(request):
    title = request.POST.get("name")
    description = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", { "title": title, "description": description})

def submit_edit(request):
    title = request.POST.get("name")
    description = request.POST.get("description")

    util.save_entry(title, description)

    return render(request, "encyclopedia/edit.html", { "title": title, "description": description})

def random_entry(request):
    entries = util.list_entries()
    index = random.randrange(len(entries))
    title = entries[index]

    return render(request, "encyclopedia/entry.html", {"entry": markdown(util.get_entry(title)), "title": title, })

