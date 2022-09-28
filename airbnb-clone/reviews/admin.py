from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from reviews.models import Review


class SpecialKeywordFilter(SimpleListFilter):
    title = "특정 단어 빠른 검색"
    parameter_name = "keyword"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("hello", "Hello"),
            ("wow", "Wow"),
        ]

    def queryset(self, request, queryset: Review):
        keyword = self.value()
        if keyword:
            return queryset.filter(payload__contains=keyword)
        else:
            return queryset


class GoodOrBadFilter(SimpleListFilter):
    title = "좋은 리뷰 Or 나쁜 리뷰"
    parameter_name = "point"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset: Review):
        point = self.value()
        if point == "good":
            return queryset.filter(rating__gte=3)
        elif point == "bad":
            return queryset.filter(rating__lt=3)
        else:
            return queryset


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        "rating",
        SpecialKeywordFilter,
        GoodOrBadFilter,
    )
