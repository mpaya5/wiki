import random

from django import forms
from django.shortcuts import render

from . import util

from markdown2 import Markdown

markdwn = Markdown()

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'myfieldclass',
        'placeholder': 'Search'
        }))

def index(request):
    entries = util.list_entries()
    searched = []
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Search(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdwn.convert(page)

                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }

                    return render(request, "encyclopedia/entry.html", context)
                if item.lower() in i.lower(): 
                    searched.append(i)
                    context = {
                        'searched': searched, 
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)

        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    else:
        return render(request, 'encyclopedia/index.html', {
            "entries": util.list_entries(),
            "form": Search()
        })
        

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdwn.convert(page) 
        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})
