from .models import Board
from django.shortcuts import render, redirect


def lobby(request):
    if not request.session.session_key:
        request.session.create()
    boards = Board.objects.all()
    return render(
        request, "board/lobby.html", {"session_id": request.session.session_key, "boards":boards}
    )

def board(request, board=None):
    if not request.session.session_key:
        return redirect("/")
    
    boards = Board.objects.all()

    return render(
        request, "board/board.html",{"boards":boards}
    )
    
