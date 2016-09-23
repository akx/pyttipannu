from django.http.response import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import UpdateView

from recipes.models import Recipe


class Index(TemplateView):
    template_name = 'recipes/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()
        context.update(
            newest_recipes=Recipe.objects.public().order_by('-id')[:10],
        )
        return context


class Submit(CreateView):
    model = Recipe
    fields = ('name', 'content')
    template_name = 'recipes/submit.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class Show(DetailView):
    model = Recipe
    template_name = 'recipes/view.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.visible_to(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            can_edit=self.can_edit(),
            can_rate=self.can_rate(),
            rating_range=range(1, 6),
        )
        if self.can_rate():
            context.update(
                my_rating=self.object.ratings.filter(rater=self.request.user).first(),
            )
        return context

    def can_rate(self):
        return bool(self.request.user.is_authenticated)

    def can_edit(self):
        return (self.object.creator == self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        public_flag = request.POST.get('public')
        if self.can_edit() and public_flag:
            self.object.public = (public_flag == '1')
            self.object.save()
        rating = request.POST.get('rating')
        if self.can_rate() and rating:
            try:
                rating = int(rating)
                if not 1 <= rating <= 5:
                    raise ValueError()
            except (TypeError, ValueError):
                pass
            self.object.ratings.update_or_create(
                rater=self.request.user,
                defaults={'rating': rating},
            )

        return HttpResponseRedirect(self.request.path)


class Edit(UpdateView):
    model = Recipe
    fields = ('name', 'content')
    template_name = 'recipes/submit.html'

    def get_queryset(self):
        return super(Edit, self).get_queryset().filter(creator=self.request.user)


class List(ListView):
    model = Recipe
    context_object_name = 'recipes'
    queryset = Recipe.objects.public()
    template_name = 'recipes/list.html'

    def get_queryset(self):
        return Recipe.objects.visible_to(self.request.user).select_related('creator')
