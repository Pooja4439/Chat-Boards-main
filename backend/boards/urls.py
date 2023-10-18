from django.urls import path,include
from .views import  lobby, board


urlpatterns = [
    path('', lobby, name = "lobby-room"),
    path('board/<str:board>', board, name="board-room"),
    path('board/<str:board>/connect/', include('ChatBoard.urls'), name = 'board-room-chat'),
]