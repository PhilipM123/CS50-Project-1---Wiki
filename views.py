from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.core.files.storage import default_storage


from . import util
import random
import markdown2
#C:\Users\pilpo\AppData\Local\Programs\Python\Python310.


class NewEntryForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )

def topic(request, title):
    topic_ = util.get_entry(title)
    if topic_:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(topic_)
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: Wiki page titled '{title}' not found",
            "title": title
        })


def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def search(request):
    query = request.GET.get("q","")
    topic_ = util.get_entry(query)
    if topic_:
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": markdown2.markdown(topic_)
        })
    else:
        entries = util.list_entries()
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": entries
        })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntryForm()
        })
    
    form = NewEntryForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        filename = f"entries/{title}.md"
        content = form.cleaned_data.get("content")
    else:
        messages.add_message(
        request, messages.WARNING, message="Invalid request form"
        )
    if default_storage.exists(filename):
        return render(request, "encyclopedia/new_page_error.html", {
            "title": title
        })
    else:
        util.save_entry(title, content)
        return topic(request, title)


def edit_page(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = NewEntryForm({
            "title": title,
            "content": content    
            })
        return render(request,"encyclopedia/edit_page.html",{
            "form": form, 
            "title": title})

    form = NewEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        util.save_entry(title, content)
        return topic(request, title)

def random_page(request):
    entries = util.list_entries()
    items = len(entries)
    number = random.randint(0,items-1)
    entry = entries[number]
    return topic(request, entry)


