from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect

from . import util


class NewEntry(forms.Form):
    title = forms.CharField(label='Title')
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":5}), label='Text')



def index(request):
    search_result = []
    q = request.GET.get('q')
    entries = util.list_entries()
    if not q:
        search_result = entries
        return render(request, "encyclopedia/index.html", {
            "entries": search_result
        })
    q = q.lower()
    for entry in entries:
        if q == entry.lower():
            return HttpResponseRedirect(reverse('entry', args=[q]))
        elif q in entry.lower():
            search_result.append(entry)
    return render(request, "encyclopedia/index.html", {
        "entries": search_result
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        raise Http404('Page not found')
    else:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'entry': entry
    })


def add_entry(request):
    add_entry_form = NewEntry()
    if request.method == 'POST':
        add_entry_form = NewEntry(request.POST)
        if add_entry_form.is_valid():
            title = add_entry_form.cleaned_data['title']
            text = add_entry_form.cleaned_data['text']
            if util.get_entry(title) == None:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse('entry', args=[title]))
            else:
                messages.error(request, 'The entry with this title is already exists')
    return render(request, "encyclopedia/add.html", {
        "form": add_entry_form,
    })

