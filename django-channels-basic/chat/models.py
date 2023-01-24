from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)

    @property
    def chat_group_name(self) -> str:
        return self.make_chat_group_name(room=self)

    @classmethod
    def make_chat_group_name(cls, room=None, room_pk=None) -> str:
        return f"chat-{room.pk if room else room_pk}"

    class Meta:
        ordering = ['-id']