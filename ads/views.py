from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .owner import *
from django.views import View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from django.db.models import Q

# Create your views here.

class MainView(OwnerListView):
    model = Ad
    category_slug=None

    def get(self,request,category_slug=None):
        self.category_slug = category_slug
        return super().get(self,request,category_slug=None)
    def get_queryset(self):
        qs = super().get_queryset()
        if self.category_slug:
            sel_category = get_object_or_404(Category,slug=self.category_slug)
            qs = qs.filter(category=sel_category)
        return qs
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search',False)
        if self.category_slug:
            context['category'] = self.category_slug
        if context['search']:
            search = context['search']
            context['object_list'] = context['ad_list'] = context['object_list'].filter(Q(title__contains=search)|Q(text__contains=search))
        favorites = list()
        if self.request.user.is_authenticated:
            rows = self.request.user.favorite_ads.values('id')
            favorites = [ row['id'] for row in rows ]
        context['favorites'] = favorites
        context['categories'] = Category.objects.all()
        return context

class UserAdsView(LoginRequiredMixin,MainView):
    model = Ad
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
class AdCreate(LoginRequiredMixin,View):
    template_name = 'ads/ad_create_form.html'
    success_url = reverse_lazy('ads:all')
    def get(self,request):
        form = CreateForm()
        ctx = {
            'form':form
            }
        return render(request,self.template_name,ctx)
    def post(self,request):
        form = CreateForm(request.POST,request.FILES)
        if not form.is_valid():
            ctx = {
            'form':form
            }
            return render(request,self.template_name,ctx)
        f = form.save(commit=False)
        f.owner = request.user
        f.save()
        return redirect(self.success_url)
    pass
class AdDetail(OwnerDetailView):
    model = Ad
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('logingng: ',self.request.user,self.request.user.is_authenticated)
        x = context['object']
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')

        if self.request.user.is_authenticated:
            comment_form = CommentForm()
            context['comment_form'] = comment_form
            print('checkekekekeek:  ',context['comment_form'])
        # Call the base implementation first to get a context
        # Add in the publisher
        context['comments'] = comments
        return context
    # def get(self, request, pk) :
    #     x = Ad.objects.get(id=pk)
    #     comments = Comment.objects.filter(ad=x).order_by('-updated_at')
    #     comment_form = CommentForm()
    #     context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
    #     return render(request, self.template_name, context)
    pass

class AdUpdate(LoginRequiredMixin,View):
    template_name = 'ads/ad_update_form.html'
    success_url = reverse_lazy('ads:all')
    def get(self,request,pk):
        ins = get_object_or_404(Ad,id=pk, owner=self.request.user)
        form = CreateForm(instance=ins)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)
    def post(self, request, pk=None):
        ins = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES, instance=ins)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        mdl = form.save(commit=True)
        return redirect(self.success_url)
    pass
class AdDelete(OwnerDeleteView):
    model = Ad
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('ads:all')
    pass

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=ad)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        ad = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=ad).delete()
        except Exception as e:
            pass

        return HttpResponse()
def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
