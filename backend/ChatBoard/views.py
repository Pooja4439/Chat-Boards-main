from django.shortcuts import render

from boards.models import Board

# Create your views here.
def home(reqest,board = None):
    return render(reqest,'test.html')

# def lobby(request,board=None):
#     return render(
#         request, "board.html"
#     )