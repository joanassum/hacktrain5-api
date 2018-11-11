from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import queues.routing
application = ProtocolTypeRouter({
# (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            queues.routing.websocket_urlpatterns
        )
    ),
})
