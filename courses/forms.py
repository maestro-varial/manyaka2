from django.forms.models import inlineformset_factory
from .models import *
from parler.forms import TranslatableModelForm

# inlines = [CurriculamInline, videoInline, featuresInline, faqInline , CertificateInline]

# fields = "__all__"

class CreateMcqForm(TranslatableModelForm):
    class Meta:
        model = MCQ
        exclude = ['course','completed']


class CreateCourseForm(TranslatableModelForm):
    class Meta:
        model = Course
        exclude = ['author','hit','button_text','maincourse']


class CertificateForm(TranslatableModelForm):
    class Meta:
        model = Certificate
        exclude = ['course','created_at']

class faqForm(TranslatableModelForm):
    class Meta:
        model = faq
        fields = ['title','content']

class featuresForm(TranslatableModelForm):
    class Meta:
        model = features
        fields = ['title','content']

class videoForm(TranslatableModelForm):
    class Meta:
        model = video
        exclude = ['course','serial_number']

class CurriculamForm(TranslatableModelForm):
    class Meta:
        model = Curriculam
        exclude = ['course']
        # fields = ['title','content']


curriculam_formset = inlineformset_factory(
    Course,
    Curriculam,
    form=CurriculamForm,
    extra=1,
)

video_formset = inlineformset_factory(
    Course,
    video,
    form=videoForm,
    extra=1,
)

features_formset = inlineformset_factory(
    Course,
    features,
    form=featuresForm,
    extra=1,
)

faq_formset = inlineformset_factory(
    Course,
    faq,
    form=faqForm,
    extra=1,
)

mcq_formset = inlineformset_factory(
    Course,
    MCQ,
    form=CreateMcqForm,
    extra=1,
)