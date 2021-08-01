from rest_framework import serializers
from .models import Waste


class WasteSerrializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = ('participant', 'date', 'glass', 'wastepapper', 'plastic')
