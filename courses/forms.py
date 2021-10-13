from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from parler.forms import TranslatableModelForm

# inlines = [CurriculamInline, videoInline, featuresInline, faqInline , CertificateInline]

# fields = "__all__"
# class McqOptionFormset(TranslatableModelForm):
#     class Meta:
#         model = McqOption
#         exclude = ['mcq']
CORRECT_OPTION_CHOICES = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
]

class CreateMcqForm(TranslatableModelForm):
    option1 = forms.CharField(max_length=200, required=True)
    option2 = forms.CharField(max_length=200, required=True)
    option3 = forms.CharField(max_length=200, required=True)
    correct_option = forms.ChoiceField(choices=CORRECT_OPTION_CHOICES, required=True)


    def pre_save(self, *args, **kwargs):
        # instance = super().save(*args, **kwargs)

        correct_option = self.cleaned_data.get('correct_option')
        option1 = self.cleaned_data.get('option1')
        option2 = self.cleaned_data.get('option2')
        option3 = self.cleaned_data.get('option3')

        if option1 and option2 and option3:
            options = [
                option1,
                option2,
                option3,
            ]
            # self.instance.save()
            option_instances = []
            for index, option in enumerate(options):
                mcqOption = McqOption(
                    mcq = self.instance,
                    title = option
                )
                if int(correct_option) == index+1:
                    mcqOption.correct = True
                option_instances.append(mcqOption)
            return option_instances
        raise ValidationError("options not defined")

    def save(self, *args, **kwargs):
        option_instances = self.pre_save()
        instance = super().save(*args, **kwargs)
        # instance = super(MCQ, self).save(*args, **kwargs)

        return instance, option_instances

    class Meta:
        model = MCQ
        fields = ['title','option1','option2','option3','correct_option']
        # exclude = ['course','completed']


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