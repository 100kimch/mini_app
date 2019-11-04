from django.contrib.auth.models import User, Group
from rest_framework import serializers


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['title', 'content']
