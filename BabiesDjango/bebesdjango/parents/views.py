from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from parents.models import Parent
from parents.serializers import ParentSerializer
from babies.models import Baby
from babies.serializers import BabySerializer

from guardian.shortcuts import assign_perm
from permissions.services import APIPermissionClassFactory
# Create your views here.

class ParentViewSet(viewsets.ModelViewSet):
	queryset=Parent.objects.all()
	serializer_class=ParentSerializer

	permission_classes = (
        APIPermissionClassFactory(
            name='ParentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': True,
                    'destroy': False,
                    'update': False,
                    'partial_update': False,
                    'babies':True,
                }
            }
        ),
    )

	@action(detail=True,methods=['get'])
	def babies(self, request, pk=None):
		parent=self.get_object()
		babies = Baby.objects.filter(parent = parent)
		return Response({
			'Babies':(baby.name for baby in babies)
			})