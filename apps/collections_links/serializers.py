from rest_framework import serializers

from apps.collections_links.models import Collection, Link


class CollectionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'id', 'name', 'url',
        ]

