import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from boards.models import Board
from posts.models import Posts

class BoardNotExistsException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.board_name = self.scope['url_route']['kwargs']['board_name'].title()
            self.board_id = Board.objects.get(board_name = self.board_name).id
            self.user_id = self.scope["session"].session_key
            self.posts_40 = Posts.objects.filter(board_id = self.board_id).order_by('-post_time')
            self.posts_40 = list(self.posts_40.values()[:40])
            serialized_posts = json.dumps(self.posts_40, cls=DjangoJSONEncoder)
            self.room_group_name = self.board_name

            async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)

            self.accept()
            self.send(json.dumps(
                {'posts':serialized_posts}
            ))

        except BoardNotExistsException:
            self.accept()
            self.send(json.dumps(
                {'error':'Board does not exists.'}
            ))
            self.close(code=401)

        except Exception as e:
            raise e
        
    def receive(self, text_data):
        # recieve some data and put save it in model posts and return the data to the group
        self.board_name = self.scope['url_route']['kwargs']['board_name'].title()
        self.board_id = Board.objects.get(board_name = self.board_name).id

        model_posts = Posts(board_id_id = self.board_id,post_content = text_data)
        model_posts.save()

        response_data = {
            'content': model_posts.post_content,
            'date': model_posts.post_date.strftime("%Y-%m-%d"),
            'time': model_posts.post_time.strftime("%H:%M:%S"),
        }

        # self.channel_layer.send(json.dumps(response_data, cls=DjangoJSONEncoder))

        async_to_sync(self.channel_layer.group_send)('{}'.format(self.board_id),
                                                     {
                                                         'new_post_{}'.format(self.board_name):json.dumps(response_data,cls=DjangoJSONEncoder)
                                                     })

    def chat_message(self,event):
        print(event)
        # message = event['message']
        # board_id = event['board_id']
        # self.send(
        #     json.dumps(
        #     {
        #         'type':chat_message,
        #         'board_id':board_id,
        #         'message':message,
        #     }
        #     )
        # )

    def disconnect(self, code):
        return super().disconnect(code)