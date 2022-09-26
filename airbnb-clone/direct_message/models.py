from django.db import models
from common.models import BaseTimeTamplate
from django.contrib.auth import get_user_model


class ChattingRoom(BaseTimeTamplate):
    """메시지 룸"""

    user = models.ManyToManyField(get_user_model())

    def __str__(self) -> str:
        return "Chatting Room"


class Message(BaseTimeTamplate):
    """메시지 모델링"""

    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    room = models.ForeignKey("direct_message.ChattingRoom", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
