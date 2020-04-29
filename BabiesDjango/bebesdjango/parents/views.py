from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from parents.models import Parent
from parents.serializers import ParentSerializer
from babies.models import Baby
from babies.serializers import BabySerializer

# Create your views here.

class ParentViewSet(viewsets.ModelViewSet):
	queryset=Parent.objects.all()
	serializer_class=ParentSerializer

	@action(detail=True,methods=['get'])
	def babies(self, request, pk=None):
		parent=self.get_object()
		babies = Baby.objects.filter(parent = parent)
		return Response({
			'Babies':(baby.name for baby in babies)
			})