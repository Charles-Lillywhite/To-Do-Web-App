# todo_list/todo_app/models.py

# IMPORT NECESSARY PACKAGES

from django.utils import timezone
from django.db import models
from django.urls import reverse


# DEFINE A STAND-ALONE FUNCTION, which we can use for due-dates

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


# DEFINE MODEL CLASSES
# they inherit from django.db.models.Model superclass, which does
# most of the heavy lifting 
# we just need to defn the data fields in each model (ie title etc)
# we have two types of data item (model): list, and item, with each item belonging to a list

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True) # must be unique with maximum a length

    def get_absolute_url(self):   # Django convention for data models
        return reverse("list", args=[self.id]) # this method returns the URL for a given data item (note that id is automatically defined by Model superclass, and is unique for each object)
                                               # reverse() avoids hard-coding the URL and its params

    def __str__(self):  # standard dunder method for enabling print(a_class)
        return self.title

class ToDoItem(models.Model):  # again, we inherit from models superclass
    title = models.CharField(max_length=100) 
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True) # added time is now
    due_date = models.DateTimeField(default=one_week_hence) # default due date uses our stand-alone function
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE) # This links the ToDoItem object back to the ToDoList object (foreign key relationship)! .CASCADE in on_delete means that deleting a ToDoList deletes all ToDoItems in that list.

    def get_absolute_url(self):  # Django convention for data models
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):   # standard dunder method for enabling print(a_class)
        return f"{self.title}: due {self.due_date}"

    class Meta: # Use NESTED Meta class to set some useful options (ordering here) 
        ordering = ["due_date"]

 

# TextField used for longer strings, CharField for shorter
# DateTimeField is AISOTT
