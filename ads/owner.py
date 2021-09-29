from django.views.generic import CreateView,UpdateView, DeleteView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerListView(ListView):
    pass
class OwnerDetailView(DetailView):
    pass
class OwnerCreateView(LoginRequiredMixin,CreateView):
    def form_valid(self,form):
        object = form.save(commit=False)
        object.owner = self.request.user
        return super(OwnerCreateView,self).form_valid(form)
class OwnerUpdateView(LoginRequiredMixin,UpdateView):
    #query set contain the model instance of the given pk
    #so it'll return the instance but we need to make sure only the one where user macth username is return
    #so we'll filter trough id the user macthed
    def get_queryset(self):
        qs = super(OwnerUpdateView,self).get_queryset()
        return qs.filter(owner=self.request.user)
    pass
class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    #similar to updateview
    def get_queryset(self):
        qs = super(OwnerDeleteView,self).get_queryset()
        return qs.filter(owner=self.request.user)
    pass
