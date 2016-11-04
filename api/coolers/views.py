from coolers.models import Cooler
from coolers.serializers import CoolerSerializer
from coolers.serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from coolers.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view, permission_classes
from coolers.permissions import IsOwnerOrReadOnly
from django.views.decorators.gzip import gzip_page
import os
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import numpy
import higlass_getter as hgg
from tiles import makeTile
from itertools import chain
from django.db.models import Q

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'coolers': reverse('cooler-list', request=request, format=format)
    })

@method_decorator(gzip_page, name='dispatch')
class CoolersViewSet(viewsets.ModelViewSet):
    """
    Coolers
    """
    def get_queryset(self):
        queryset = super(CoolersViewSet, self).get_queryset()
	publicQSet = Cooler.objects.filter(public=True)
        
	if self.request.user.is_authenticated():
            	if not self.request.user.is_staff:
			queryset = queryset.filter(Q(owner=self.request.user) | Q(public=True))
			#queryset = querysetPrivate+publicQSet
			#queryset = list(chain(publicQSet,querysetPrivate))
	else:
		queryset = publicQSet

        return queryset

    queryset = Cooler.objects.all()
    serializer_class = CoolerSerializer
    #permission_classes = (IsOwnerOrReadOnly,)	

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])    
    def tileset_info(self, request, *args, **kwargs):
	cooler = self.get_object()
	info = hgg.getInfo("data/"+cooler.processed_file)
	od = {}
	od["_source"] = {}
	od["_source"]["tile_value"] = info
	od["_source"]["tile_id"] = "tileset_info"
	return JsonResponse(od, safe=False)
  
    @method_decorator(gzip_page, name='dispatch') 
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def tiles(self, request, *args, **kwargs):
		cooler = self.get_object()
		infod = hgg.getInfo("data/"+cooler.processed_file)
		"""
		outputMatrices = []
		zoom=request.GET["zoom"]
		xpos=request.GET["xpos"]
		ypos=request.GET["ypos"]
		zooma = zoom.split(',')
		xposa = xpos.split(',')
		yposa = ypos.split(',')
		numMats = len(zooma)
		for matIdx in range(0,numMats):
			outputMatrices.append(map(lambda x: float("{0:.1f}".format(x)),makeTile(int(zooma[matIdx]),int(xposa[matIdx]),int(yposa[matIdx]),cooler.processed_file)))
		"""
	 	hargs = request.GET.getlist("d")

                print("hargs:", hargs)

                ret_dict = {}

                for harg in hargs:
                    prea = harg.split('.')
                    argsa = map(lambda x:int(x), prea)

                    ret_dict[harg] = {}
                    ret_dict["dense"] = map(lambda x: float("{0:.1f}".format(x)),makeTile(argsa[0],argsa[1],argsa[2],cooler.processed_file))
                    ret_dict["min_value"] = min(ret_dict["dense"])
                    ret_dict["max_value"] = max(ret_dict["dense"])

		return JsonResponse(ret_dict,safe=False) 

    
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def generate_tiles(self, request, *args, **kwargs):
        cooler = self.get_object()
	serializer = CoolerSerializer(cooler,data=request.data)
        cooler.rawfile_in_db = True
	idv = cooler.id
	#os.system("source activate snakes")
	os.system("wget "+cooler.url)	
        urlval = cooler.url.split('/')[-1]
	os.system("mv "+str(urlval)+" data/"+str(urlval).lower())
	urlval = urlval.lower()
	os.system("python recursive_agg_onefile.py data/"+urlval)
	cooler.processed_file = '.'.join(urlval.split('.')[:-1])+".multires.cool"
	cooler.processed = True
	cooler.save()
	return HttpResponseRedirect("/coolers/")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users
    """
    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()

        if self.request.user.is_staff:
                queryset = queryset
	elif self.request.user.is_authenticated():
                queryset = queryset.filter(username=self.request.user)
	else:
	    queryset = User.objects.none()

        return queryset
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
