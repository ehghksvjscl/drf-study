from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_room_set",
    )
    name = models.CharField(max_length=100)

    @property
    def chat_group_name(self) -> str:
        return self.make_chat_group_name(room=self)

    @classmethod
    def make_chat_group_name(cls, room=None, room_pk=None) -> str:
        return f"chat-{room.pk if room else room_pk}"

    class Meta:
        ordering = ['-id']

def post__on_post_delete(instance: Room, **kwargs):
    async_to_sync(get_channel_layer().group_send)(
        instance.chat_group_name,
        {
            'type': 'chat.room.deleted',
        }
    )

post_delete.connect(
    post__on_post_delete,
    sender=Room,
    dispatch_uid='post__on_post_delete'
)