from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.collections_links.models import Collection, Link
from apps.collections_links.serializers import CollectionSerializer, LinkSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    # this sets current user as author of the collection
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # this filters user's collections
    def get_queryset(self):
        user = self.request.user
        return Collection.objects.filter(user=user)

    # this represents collection/<pk>/links endpoint
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def links(self, request, *args, **kwargs):
        col_id = kwargs['pk']
        collection = Collection.objects.get(id=col_id)

        # check if the collection belongs to the current user
        if collection.user.id != request.user.id:
            return Response({'message': 'not found'}, status=404)

        if request.method == 'GET':
            links = Link.objects.filter(collection=collection)
            serializer = LinkSerializer(links, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = LinkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(collection=collection)
                return Response(serializer.data)
            return Response(serializer.errors)

    # this represents collection/<pk>/links/<link_id> endpoint
    @action(detail=True, methods=['GET', 'PUT', 'PATCH', 'DELETE'], permission_classes=[IsAuthenticated],
            url_path="links/(?P<link_id>[^/.]+)",  url_name='get_put_patch_delete_link')
    def link(self, request, **kwargs):
        collection_id = int(kwargs['pk'])
        link_id = kwargs['link_id']
        collection = Collection.objects.get(id=collection_id)
        link = Link.objects.get(id=link_id)

        # check if the collection belongs to the current user
        if collection.user.id != request.user.id:
            return Response({'message': 'not found'}, status=404)

        # checks if the link belongs to the collection
        if link.collection.id != collection_id:
            return Response(
                {'message': 'link id - ' + str(link_id) + ' not found in collection id - ' + str(collection_id)}, status=404)

        if request.method == 'GET':
            serializer = LinkSerializer(link)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = LinkSerializer(link, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

        elif request.method == 'PATCH':
            serializer = LinkSerializer(link, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

        elif request.method == 'DELETE':
            link.delete()
            return Response(status=204)


