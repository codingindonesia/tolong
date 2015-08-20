from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Case, Responder, Response, Invitation
from .form import InvitationForm
from .serializers import CaseSerializer, ResponderSerializer, ResponseSerializer
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import mixins, viewsets
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib import messages

# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class LoginView(TemplateView):
    template_name = 'home/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the account
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))

        return render(request,self.template_name)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class HomeView(TemplateView):
    template_name = 'home/index.html'
    def get(self, request):
        form = InvitationForm()
        return render(request,self.template_name, {'form':form})

    def post(self, request):
        invitation = None
        form = InvitationForm(request.POST or None, instance=invitation)
        if form.is_valid():
            form.save()
            messages.success(request,'Thank you for your support. We will contact you once we are ready.')
            return HttpResponseRedirect(reverse('thankyou'))
        else:
            return render(request, self.template_name, {'form':form})

class ThankYouView(TemplateView):
    template_name = 'home/thankyou.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class DashboardView(TemplateView):
    template_name = 'case/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class InvitationsView(TemplateView):
    template_name = 'home/invitations.html'

    def get(self, request, *args, **kwargs):
        invitations = Invitation.objects.all()
        return render(request,self.template_name,{'invitations':invitations})

class CaseAllView(TemplateView):
    template_name = 'case/all.html'

    def get(self, request, *args, **kwargs):
        cases = Case.objects.all()
        return render(request, self.template_name, {'cases': cases})


class CaseDetailView(TemplateView):
    template_name = 'case/detail.html'
    case_id = None

    def get(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        return render(request, self.template_name, {'case': case})

#api
class CaseListApi(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class CaseDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class CasesViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all();
    serializer_class = ResponseSerializer

class ResponseApi(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

