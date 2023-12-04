from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import MessageModel
from .forms import ChangeStatusForm, CreateTasksForm
from message.tasks import message_task, task_maker
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone


def messages_page(request, *args, **kwargs) :
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
    return render(request, "messages.html", context = {"message":message_deleted, "todos": MessageModel.objects.all(), "form":ChangeStatusForm})


def not_done_tasks_page(request) :
    return render(request, "not_done_tasks.html", context={"tasks": MessageModel.objects.all()})


def done_tasks_page(request) :
    return render(request, "done_tasks.html", context={"tasks": MessageModel.objects.all()})


def not_important_tasks_page(request) :
    return render(request, "not_important_tasks.html", context={"tasks": MessageModel.objects.all()})


def important_tasks_page(request) :
    return render(request, "important_tasks.html", context={"tasks": MessageModel.objects.all()})


def create_tasks_page(request) :
    if request.method == "POST" :
        form = CreateTasksForm(request.POST)
        if form.is_valid() :
            print("the form is valid")
            MessageModel.objects.create(
                text=request.POST.get("text_input"),
                types=request.POST.get("types_of_tasks"), 
                datetime_notification=request.POST.get("date"), 
                important=request.POST.get("important")
            )
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
    return render(request, "delete_tasks.html", context={"pk":pk})


def delete_permanently_tasks_page(request, pk) :
    model = MessageModel.objects.get(id=pk)
    model_name=model.text
    model.delete()
    messages.add_message(request, messages.INFO, model_name)
    return redirect("/")