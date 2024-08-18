from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    return render(request, 'jerrysNotebook/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('dataAdded')
    context = {'topics': topics}
    return render(request, 'jerrysNotebook/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('dataAdded')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'jerrysNotebook/topic.html', context)

@login_required
def newTopic(request):
    if request.method != 'POST':
        form = TopicForm() #未提交表单，创建新表
    else:
        form = TopicForm(data=request.POST) #提交新数据
        if form.is_valid():
            newTopic = form.save(commit=False)
            newTopic.owner = request.user
            newTopic.save()
            return redirect('jerrysNotebook:topics')

    context = {'form': form}
    return render(request, 'jerrysNotebook/newTopic.html', context)

@login_required
def newEntry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm() #未提交表单，创建新表
    else:
        form = EntryForm(data=request.POST) #提交新数据
        if form.is_valid():
            newEntry = form.save(commit=False)
            newEntry.topic = topic
            newEntry.save()
            return redirect('jerrysNotebook:topic', topic_id=topic_id)
    context = {'form': form, 'topic': topic}
    return render(request, 'jerrysNotebook/newEntry.html', context)

@login_required
def editEntry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry) #未提交表单，创建新表
    else:
        form = EntryForm(instance=entry, data=request.POST) #提交新数据
        if form.is_valid():
            form.save()
            return redirect('jerrysNotebook:topic', topic_id=topic.id)
    context = {'form': form, 'entry': entry, 'topic': topic}
    return render(request, 'jerrysNotebook/editEntry.html', context)