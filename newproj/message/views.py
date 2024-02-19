from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import MessageModel, ChatIds
from .forms import ChangeStatusForm, CreateTasksForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone
from message.tasks import todo_notification
from datetime import date, datetime
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
import requests

def messages_page(request, *args, **kwargs) :
    # bot.send_task_notification("hi")
    storage = messages.get_messages(request) 
    
    message_deleted = False
    for message in storage :
        message_deleted = message 
        break
    if request.method == "POST" :
        message = get_object_or_404(MessageModel, pk=request.POST.get("pk"))
        message.is_done = not message.is_done
        message.important = not message.is_done
        message.save()
    return render(request, "messages.html", context = {"message":message_deleted, "todos": MessageModel.objects.all(), "form":ChangeStatusForm, "now":timezone.now(), "two_hours":timedelta(hours=2)})


def not_done_tasks_page(request) :
    return render(request, "not_done_tasks.html", context={"tasks": MessageModel.objects.all()})


def done_tasks_page(request) :
    return render(request, "done_tasks.html", context={"tasks": MessageModel.objects.all()})


def not_important_tasks_page(request) :
    return render(request, "not_important_tasks.html", context={"tasks": MessageModel.objects.all()})


def important_tasks_page(request) :
    return render(request, "important_tasks.html", context={"tasks": MessageModel.objects.all()})


def chat_id_view(request) :
    ChatIds.objects.create(
        chat_id=request.GET["chat_id"]
    )
    print("chat_id saved successfully")
    print(request.GET)
    return redirect("/")
    

def bot_send_notification(text) :
    r = requests.post("https://api.telegram.org/bot6716709020:AAF_77A_Bu3_woJBYnpZizM8X4kZGe2DjJs/sendMessage", 
        data={"chat_id":int(ChatIds.objects.all()[0].chat_id), "text": text}
    )
    print(ChatIds.objects.all()[0].chat_id)
    print(r)

    
def create_tasks_page(request) :
    if request.method == "POST" :
        form = CreateTasksForm(request.POST)
        if form.is_valid() :
            print("the form is valid")
            MessageModel.objects.create(
                text=request.POST.get("text_input"),
                types=request.POST.get("types_of_tasks"), 
                datetime_notification = make_aware(datetime.strptime(request.POST.get("date"), '%Y-%m-%d %H:%M:%S')), 
                important=request.POST.get("important")
            )
            print(request.POST.get("date"))
            todo_notification.apply_async((request.POST.get("text_input"), request.POST.get("types_of_tasks"), request.POST.get("date"), request.POST.get("important")), eta=make_aware(datetime.strptime(request.POST.get("date"), '%Y-%m-%d %H:%M:%S')))
            return redirect("main_page")
            
        message = request.POST.get("date")
        print(message)
    else :
        form = CreateTasksForm()
    return render(request, "create_tasks.html", context={"form":form})


def edit_tasks_page(request, pk) :
    model = MessageModel.objects.get(id=pk)
    if request.method == "POST" :
        form = CreateTasksForm(request.POST)
        if form.is_valid() :
            print("the form is valid")
            model.text=request.POST.get("text_input")
            model.types=request.POST.get("types_of_tasks")
            model.datetime_notification=request.POST.get("date")
            model.important=request.POST.get("important")
            model.save()
            return redirect("main_page")
        message = request.POST.get("date")
        print(message)
    else :
        print(MessageModel.objects.get(id=pk))
        form = CreateTasksForm(initial={"text_input": model.text, "types_of_tasks": model.types, "date": model.datetime_notification, "important":model.important})
    return render(request, "create_tasks.html", context={"form":form})


def delete_tasks_page(request, pk) :
    # TODO make this a POST request
    return render(request, "delete_tasks.html", context={"pk":pk})


def delete_permanently_tasks_page(request, pk) :
    # TODO make this a POST request
    model = MessageModel.objects.get(id=pk)
    model_name=model.text
    model.delete()
    messages.add_message(request, messages.INFO, model_name)
    return redirect("/")