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
    return user.username == obj.parent.name

class BabyViewSet(viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'babies.view_baby',
                    'destroy': True,
                    'update': True,
                    'partial_update': True,
                    'events':is_parent
                }
            }
        ),
    )

    def perform_create(self, serializer):
        parent=name=serializer.validated_data['parent'].username
        user = self.request.user
        print(str(user))
        print(str(parent))
        if(str(user)==str(parent)):
            baby = serializer.save()
            print("Se creó")
            user = self.request.user
            assign_perm('babies.view_baby', user, baby)
            return Response(serializer.data)
        elif(str(user)!=str(parent)):
            print("No tiene autorización")

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        baby = self.get_object()
        events = Event.objects.filter(baby = baby)
        return Response({
            'Events':(event.event_type for event in events)
            })
