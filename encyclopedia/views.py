from django.shortcuts import render
import markdown2
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    content = markdown2.markdown(content)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content    
        })

def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content    
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content    
        })

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        page = util.get_entry(title)
        if page is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists.",
            })
        else:
            util.save_entry(title, content)
            content = markdown2.markdown(content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content    
            })

def rand(request):
    if request.method == "GET":
        all = util.list_entries()
        page = random.choice(all)
        content = util.get_entry(page)
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
                "title": page,
                "content": content    
            })

def search(request):
    search = request.GET.get('q', '')
    page = util.get_entry(search)
    
    if page is not None:
        page = markdown2.markdown(page)
        return render(request, "encyclopedia/entry.html", {
                "title": search,
                "content": page    
            })
    else:
        rec = []
        for entry in util.list_entries():
            if search.lower() in entry.lower():
                rec.append(entry)
        return render(request, "encyclopedia/search.html", {
                "rec": rec    
            })
