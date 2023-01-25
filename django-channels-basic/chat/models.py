from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from mysite.json_extended import ExtendedJSONDecoder, ExtendedJSONEncoder


class OnlineUserMixin(models.Model):
    class Meta:
        abstract = True

    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RoomMember",
        blank=True,
        related_name="joined_room_set"
    )

    def get_online_users(self):
        return self.online_user_set.all()

    def get_online_usernames(self):
        return list(self.online_user_set.values_list('username', flat=True))

    def is_joined_user(self, user):
        return self.get_online_users().filter(pk=user.pk).exists()

    def user_join(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)

        is_new_join = len(room_member.channel_names) == 0
        room_member.channel_names.add(channel_name)

        if room_member.pk is None:
            room_member.save()
        else:
            room_member.save(update_fields=['channel_names'])

        return is_new_join

    def user_leave(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            return True

        room_member.channel_names.remove(channel_name)
        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member.save(update_fields=['channel_names'])
            return False


class Room(OnlineUserMixin, models.Model):
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

class RoomMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    channel_names = models.JSONField(
        default=set,
        encoder=ExtendedJSONEncoder,
        decoder=ExtendedJSONDecoder,
        )