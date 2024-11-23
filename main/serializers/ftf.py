# serializers/ftf.py

from rest_framework import serializers
from ..models.ftf import FTF

class FTFSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTF
        fields = ['id', 'name']
