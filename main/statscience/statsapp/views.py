from django.http import HttpRequest
from django.shortcuts import render
import os

proj_cwd = os.getcwd()  # ./main/statscience
app_name = "statsapp"

templates_dir = os.path.join(proj_cwd, "assets", app_name, "templates")

def home(request: HttpRequest):
    return render(request, f'{os.path.join(templates_dir, 'home.html')}')