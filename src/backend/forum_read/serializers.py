from rest_framework import serializers

from .models import *


class ThreadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadCategory
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class ThreadVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadVote
        fields = '__all__'


class TaggedThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedThread
        fields = '__all__'
