from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "is_published")
    fields = ('title', 'slug', 'content', 'preview', 'is_published')
    prepopulated_fields = {
        "slug": ["title"],
    }

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели
        """
        if not change:  # Проверяем что запись только создаётся
            obj.author = request.user

        super(ArticleAdmin, self).save_model(
            request=request, obj=obj, form=form, change=change
        )
