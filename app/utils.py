from django.db.models import Count

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]

from .models import Tag

class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        tags = Tag.objects.top_tags()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['tags'] = tags

        if 'tag_selected' not in context:
            context['tag_selected'] = 0

        return context

