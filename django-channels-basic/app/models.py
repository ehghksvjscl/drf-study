from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, post_delete

from app.mixins import ChannelLayerGroupSendMixin

class Post(ChannelLayerGroupSendMixin, models.Model):
    CHANNEL_LAYER_GROUP_NAME = 'liveblog'

    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ['-id']

    
def post__on_post_save(instance: Post, created: bool, **kwargs):
    if created:
        message_type = 'liveblog_post_created'
    else:
        message_type = 'liveblog_post_updated'

    post_id = instance.id
    post_partial_url = reverse('post-partial', args=[post_id])

    instance.channel_layer_group_send({
        'type': message_type,
        'post_id': post_id,
        'post_partial_url': post_partial_url
    })

post_save.connect(
    post__on_post_save,
    sender=Post,
    dispatch_uid='post__on_post_save'
)


def post__on_post_delete(instance: Post, **kwargs):
    post_id = instance.id

    instance.channel_layer_group_send({
        'type': 'liveblog_post_deleted',
        'post_id': post_id
    })

post_delete.connect(
    post__on_post_delete,
    sender=Post,
    dispatch_uid='post__on_post_delete'
)