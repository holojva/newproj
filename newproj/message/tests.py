from django.test import TestCase
from message.models import MessageModel
from django.utils import timezone
from django.db.utils import IntegrityError
from django.forms import ValidationError
from message.forms import CreateTasksForm
from django.test import Client
# Create your tests here.

class ModelTest(TestCase):

    def test_correct_model_fulfillness(self):
        """Models are perfectly and correctly fulfilled"""
        datetime_notification = timezone.now()
        text = "test model text"
        types = 1 # Работа
        is_done = False
        important = True
        message = MessageModel.objects.create(datetime_notification=datetime_notification, text=text, types=types, is_done=is_done, important=important)
        self.assertEqual(datetime_notification, message.datetime_notification)
        self.assertEqual(text, message.text)
        self.assertEqual(types, message.types)
        self.assertEqual(is_done, message.is_done)
        self.assertEqual(important, message.important)
        if is_done :
            is_done_text = "Сделано"
        else :
            is_done_text = "Не сделано"
        self.assertEqual(str(message.types) + " - " + message.text + " - " + is_done_text, message.__str__())
        with self.assertRaises(IntegrityError):
            MessageModel.objects.create(text=text, types=types, is_done=is_done, important=important)
        

    def test_ordering(self) :
        datetime_notification = timezone.now()
        text = "test model text"
        types = 1 # Работа
        # Создание моделей с разными характеристиками
        is_done = False
        important = True
        important_not_done = MessageModel.objects.create(datetime_notification=datetime_notification, text=text, types=types, is_done=is_done, important=important)
        
        important=False
        not_important_not_done = MessageModel.objects.create(datetime_notification=datetime_notification, text=text, types=types, is_done=is_done, important=important)
        
        important=True
        is_done=True
        important_done = MessageModel.objects.create(datetime_notification=datetime_notification, text=text, types=types, is_done=is_done, important=important)
        
        important=False
        not_important_done = MessageModel.objects.create(datetime_notification=datetime_notification, text=text, types=types, is_done=is_done, important=important)
        
        # проверка их ордеринга
        self.assertEqual(MessageModel.objects.all()[0], important_not_done)
        self.assertEqual(MessageModel.objects.all()[1], not_important_not_done)
        self.assertEqual(MessageModel.objects.all()[2], important_done)
        self.assertEqual(MessageModel.objects.all()[3], not_important_done)

class FormTest(TestCase) :
    def setUp(self):
        self.datetime_notification = timezone.now()
        self.text = "test model text"
        self.types = 1 # Работа
        self.is_done = False
        self.important = True
        self.message = MessageModel.objects.create(datetime_notification=self.datetime_notification, text=self.text, types=self.types, is_done=self.is_done, important=self.important)
        
    def test_create_form(self) :
        form = CreateTasksForm(initial={
            "text_input": self.text, 
            "types_of_tasks": self.types, 
            "date": "invalid data", 
            "important":self.important
        })
        self.assertFalse(form.is_valid())
        form = CreateTasksForm(initial={
            "text_input": 0, 
            "types_of_tasks": "invalid_data", 
            "date": "invalid data", 
            "important":"invalid_data"
        })
        self.assertFalse(form.is_valid())
class UrlsTest(TestCase) :
    def test_messages(self) :
        c = Client()
        response = c.get("")
        self.assertTemplateUsed(response=response, template_name="messages.html")
    def test_not_done_tasks_page(self) :
        c = Client()
        response = c.get("/not_done_tasks/")
        self.assertTemplateUsed(response=response, template_name="not_done_tasks.html")
    def test_done_tasks_page(self) :
        c = Client()
        response = c.get("/done_tasks/")
        self.assertTemplateUsed(response=response, template_name="done_tasks.html")
    def test_create_tasks_page(self) :
        c = Client()
        for i in range(40) :
            response = c.get("/create_tasks/"+str(i)+"/")
            if response.status_code == 200 :
                self.assertTemplateUsed(response=response, template_name="create_tasks.html")
    def test_edit_tasks_page(self) :
        c = Client()
        for i in range(40) :
            try :
                response = c.get("/edit/"+str(i)+"/")
                if response.status_code == 200 :
                    self.assertTemplateUsed(response=response, template_name="edit_tasks_page.html")
            except MessageModel.DoesNotExist :
                pass
            
    def test_important_tasks_page(self) :
        c = Client()
        response = c.get("/important_tasks/")
        self.assertTemplateUsed(response=response, template_name="important_tasks.html")
    def test_not_important_tasks_page(self) :
        c = Client()
        response = c.get("/not_important_tasks/")
        self.assertTemplateUsed(response=response, template_name="not_important_tasks.html")
    def test_delete_tasks_page(self) :
        c = Client()
        for i in range(40) :
            response = c.get("/delete/"+str(i)+"/")
            if response.status_code == 200 :
                self.assertTemplateUsed(response=response, template_name="delete_tasks.html")
class UrlsTest(TestCase) :
    def test_messages(self) :
        c = Client()
        response = c.get("")
        self.assertTemplateUsed(response=response, template_name="messages.html")
    def test_not_done_tasks_page(self) :
        c = Client()
        response = c.get("/not_done_tasks/")
        self.assertTemplateUsed(response=response, template_name="not_done_tasks.html")
    def test_done_tasks_page(self) :
        c = Client()
        response = c.get("/done_tasks/")
        self.assertTemplateUsed(response=response, template_name="done_tasks.html")
    def test_create_tasks_page(self) :
        c = Client()
        for i in range(40) :
            response = c.get("/create_tasks/"+str(i)+"/")
            if response.status_code == 200 :
                self.assertTemplateUsed(response=response, template_name="create_tasks.html")
    def test_edit_tasks_page(self) :
        c = Client()
        for i in range(40) :
            try :
                response = c.get("/edit/"+str(i)+"/")
                if response.status_code == 200 :
                    self.assertTemplateUsed(response=response, template_name="edit_tasks_page.html")
            except MessageModel.DoesNotExist :
                pass
            
    def test_important_tasks_page(self) :
        c = Client()
        response = c.get("/important_tasks/")
        self.assertTemplateUsed(response=response, template_name="important_tasks.html")
    def test_not_important_tasks_page(self) :
        c = Client()
        response = c.get("/not_important_tasks/")
        self.assertTemplateUsed(response=response, template_name="not_important_tasks.html")
    def test_delete_tasks_page(self) :
        c = Client()
        for i in range(40) :
            response = c.get("/delete/"+str(i)+"/")
            if response.status_code == 200 :
                self.assertTemplateUsed(response=response, template_name="delete_tasks.html")
    