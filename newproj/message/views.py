from django.shortcuts import render
from .models import MessageModel
from .forms import ChangeStatusForm
from django.shortcuts import get_object_or_404
# Create your views here.
def messages_page(request) :
    if request.method == "POST":
        print(request.POST["pk"])
        message = get_object_or_404(MessageModel, pk=request.POST.get("pk"))
        message.is_done = not message.is_done
        message.save()
        print(message.text)
        # print(form)
        # if form.is_valid():
        #     print(form.cleaned_data)
    return render(request, "messages.html", context = {"messages": MessageModel.objects.all(), "form":ChangeStatusForm})