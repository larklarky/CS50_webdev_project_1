from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        raise Http404('Page not found')
    else:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'entry': util.get_entry(title)
    })

