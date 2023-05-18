from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from taggit.models import Tag

from .models import Entry
from .forms import EntryForm, SearchForm

from datetime import datetime, date


# https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date


def index(request):
    """The home page for the Startup Journal."""
    return render(request, 'journal_entry/index.html')


@login_required
def entries(request, tag_slug=None):
    # object_list = Entry.objects.all()
    # object_list = Entry.objects.order_by('-date_added')
    object_list = Entry.objects.filter(owner=request.user).order_by('-date_added')

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        entries = paginator.page(paginator.num_pages)
    return render(request,
                 'journal_entry/list.html', {'page': page, 'entries': entries, 'tag': tag})

@login_required
def entries_by_date(request, entry_date):
    # entries = Entry.objects.filter(date_added__date=date(2023, 1, 9))
    entry_date_string = entry_date
    entry_date = datetime.strptime(entry_date_string, "%Y-%m-%d").date()
    year, month, day = entry_date.year, entry_date.month, entry_date.day
    entries = Entry.objects.filter(owner=request.user, date_added__date=date(year, month, day))

    paginator = Paginator(entries, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        entries = paginator.page(paginator.num_pages)

    return render(request, 'journal_entry/list_by_date.html', {'page': page, 'entries': entries, 'year': year, 'month': month, 'day': day})


@login_required
def entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    # Make sure the entry belongs to the current user.
    if entry.owner != request.user:
        raise Http404

    # This for loop can be deleted. It's to illustrate how we can access tags per post.
    # use: entry.tags.all() NOT entry.tags
    for tag in entry.tags.all():
        print(tag.name)
        print(tag.slug)
        print(tag)

    return render(request,'journal_entry/detail.html', {'entry': entry})


@login_required
def new_entry(request):
    """ Process a new journal entry. """
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            # Place holder to do some fancy stuff to new_entry before saving in DB.
            new_entry.owner = request.user
            new_entry.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect('journal_entry:entries')

    # Display a blank or invalid form
    return render(request, 'journal_entry/new_entry.html', {'form':form})


@login_required
def edit_entry(request, entry_id):
    """ Edit an existing journal entry. """
    entry = Entry.objects.get(id=entry_id)
    # Make sure the entry belongs to the current user.
    if entry.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            edited_entry = form.save(commit=False)
            edited_entry.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            # return redirect('journal_entry:entries')
            return redirect('journal_entry:entry', entry_id=entry.id)

    # Display the form containing the original entry data
    return render(request, 'journal_entry/edit_entry.html', {'entry':entry, 'form':form})


@login_required
def entry_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('text', 'date_added')
            search_query = SearchQuery(query)
            # results = Entry.objects.annotate(search=SearchVector('text', 'date_added'),).filter(search=query)
            results = Entry.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(owner=request.user, search=search_query).order_by('-rank')

    return render(request, 'journal_entry/search.html', {'form':form, 'query':query, 'results':results})
