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
        user = self.request.user
        recipe = self.object
        can_rate = recipe.can_rate(user)
        context.update(
            can_edit=recipe.can_edit(user),
            can_rate=can_rate,
            rating_range=range(1, 6),
        )
        if user.is_authenticated():
            context.update(
                my_rating=recipe.ratings.filter(rater=user).first(),
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = recipe = self.get_object()
        user = self.request.user

        public_flag = request.POST.get('public')

        if recipe.can_edit(user) and public_flag:
            recipe.public = (public_flag == '1')
            recipe.save(update_fields=('public',))

        rating = request.POST.get('rating')

        if rating:
            recipe.rate(user, rating)

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
