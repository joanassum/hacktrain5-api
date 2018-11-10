import json

class QueueConsumer(WebsocketConsumer):
    def connect(self):
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            "subscribers",
            self.channel_name
        )

    def disconnect(self, close_code):
        # Leave  group
        async_to_sync(self.channel_layer.group_discard)(
            "subscribers",
            self.channel_name
        )

    # Update queue status from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        queue_status = text_data_json['queues']
        # Send queue status to subscribers
        async_to_sync(self.channel_layer.group_send)(
            "subscribers",
            {
                'type': 'queue_status',
                'queue_status': queue_status
            }
        )

    # Receive message from room group
    def queue_status(self, event):
        queue_status = event['queue_status']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'queue_status': queue_status
        }))
