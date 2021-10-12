from rest_framework import fields, serializers
from .models import Course

class CourseSerializer(serializers.Serializer):
    class Meta:
        model = Course
        fields = ['__all__']

# from parler_rest.serializers import TranslatableModelSerializer
# from parler_rest.fields import TranslatedFieldsField
# from myapp.models import Country

# class CountrySerializer(TranslatableModelSerializer):
#     translations = TranslatedFieldsField(shared_model=Country)

#     class Meta:
#         model = Country
#         fields = ('code', 'translations')

# class ArticleDetailView(TranslatableSlugMixin, DetailView):
#     model = Article
#     template_name = 'article/details.html'