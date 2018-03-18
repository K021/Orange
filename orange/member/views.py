from django.shortcuts import render

from member.models import Member


def index(request):
    return render(request, 'index.html')


def input_form(request):
    contexts = {

    }
    return


def table(request):
    contexts = {
        'members': Member.objects.all(),
    }
    return None
