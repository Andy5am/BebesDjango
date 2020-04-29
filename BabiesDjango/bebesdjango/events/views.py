from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory


from parents.models import Parent
from parents.serializers import ParentSerializer
from babies.models import Baby
from babies.serializers import BabySerializer
from events.models import Event
from events.serializers import EventSerializer

	
# # Create your views here.


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'events.view',
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        parent=name=serializer.validated_data['baby'].parent.username
        user = self.request.user
        if (str(user)!=str(parent)):
            print ("No está autorizado")
        elif(str(user)==str(parent)):
            event = serializer.save()
            print ("Se creó correctamente")
            assign_perm('events.view', user, event)
            return Response(serializer.data)       
        