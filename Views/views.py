# todo_list/todo_app/views.py
from django.urls import reverse, reverse_lazy

# import the generic Django classes needed to list, create, update and delete elements in the database

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

# import the (sub)classes we defined in todo_list/todo_app/models.py
from .models import ToDoItem, ToDoList

# Let's create our views!:

# define a View (class) to display a list of the to-do-list titles
# because we are inheriting from django.views.generic.ListView, we only need to tell
# our view two things: the data-model (class) it needs to fetch, and the name of the 
# template (HTML) that will format the view

class ListListView(ListView):
    model = ToDoList # fetch the appropriate model (class) from models.py
    template_name = "todo_app/index.html" #reference the relevant html template (in templates/todo_app/) which will format the view into a displayable form

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self): # restrict the data items returned when listing the items in a to-do-list
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"]) # only fetch the items which match the id of the list we are considering
        
        # E.g if we are listing a to-do list for 'household chores', we do not need to list the items in our 'Gym exercises' to-do list.
        # the "list_id" comes from urls.py
        
    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context
    
    # 'context' is a Python dictionary that determines what data is available for rendering. 
    # The result of .get_queryset() is automatically included in context under the key object_list, but we want the template to be able to 
    # access the todo_list object itself, and not just the items within it that were returned by the query (ie so when we list the items in the to-do list
    # we can also state which to-do list they came from

class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context

