import ast, json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import views

class QueueConsumer(WebsocketConsumer):
    def connect(self):
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            "subscribers",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave  group
        async_to_sync(self.channel_layer.group_discard)(
            "subscribers",
            self.channel_name
        )

    # Update queue status from WebSocket
    def receive(self, text_data):
        print("receive: " + text_data)
        text_data_json = ast.literal_eval(text_data)
        queue_status = text_data_json['queues']
        staff_number = text_data_json['staff_number']
        level = text_data_json['level']
        # Send queue status to subscribers
        async_to_sync(self.channel_layer.group_send)(
            "subscribers",
            {
                'type': 'queue_status',
                'queue_status': queue_status,
                'staff_number': staff_number,
                'level': level
            }
        )

    # Receive message from room group
    def queue_status(self, event):
        queue_status = event['queue_status']
        staff_number = event['staff_number']
        level = event['level']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'queue_status': queue_status,
            'staff_number': staff_number,
            'level': level
        }))
