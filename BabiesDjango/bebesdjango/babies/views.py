from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from parents.models import Parent
from parents.serializers import ParentSerializer
from babies.models import Baby
from babies.serializers import BabySerializer
from events.models import Event
from events.serializers import EventSerializer

from guardian.shortcuts import assign_perm

from permissions.services import APIPermissionClassFactory


# Create your views here.

def is_parent(user, obj, request):
    return user.username == obj.parent.username

class BabyViewSet(viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='BabyPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'babies.view',
                    'destroy': False,
                    'update': True,
                    'partial_update': False,
                    'events':is_parent
                }
            }
        ),
    )

    def perform_create(self, serializer):
        baby = serializer.save()
        parent = self.request.user
        assign_perm('babies.view', parent, baby)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        baby = self.get_object()
        events_baby=[]
        for event in Event.objects.filter(baby=baby):
            events_baby.append(EventSerializer(event).data)
        return Response(events_baby)