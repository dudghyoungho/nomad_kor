# serializers/anonymous.py

from rest_framework import serializers
from ..models.anonymous import Anonymous

class AnonymousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anonymous
        fields = ['id', 'name']
