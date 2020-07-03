from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect

from . import util


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

