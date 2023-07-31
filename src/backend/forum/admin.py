from django.contrib import admin

from .models import Thread, ThreadVote


class ThreadAdmin(admin.ModelAdmin):
    pass


class ThreadVoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadVote, ThreadVoteAdmin)
