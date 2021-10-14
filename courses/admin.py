from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline
from .models import *

# Register your models here.
# Stacked inline allow us to add multiple items in single forms


class CurriculamInline(TranslatableStackedInline):
    model = Curriculam

class featuresInline(TranslatableStackedInline):
    model = features

class faqInline(TranslatableStackedInline):
    model = faq

class CertificateInline(TranslatableStackedInline):
    model = Certificate

class videoInline(AdminVideoMixin,TranslatableStackedInline):
    model = video

class MCQInline(TranslatableStackedInline):
    model = MCQ
    exclude = ['completed']

@admin.register(Course)
class CourseAdmin(TranslatableAdmin):
    list_display = ['__str__','slug']
    inlines = [CurriculamInline, videoInline, MCQInline, featuresInline,faqInline ,CertificateInline]
    save_as =True

    class Meta:
       model = Course

# admin.site.register(Curriculam, TranslatableAdmin)
# admin.site.register(features, TranslatableAdmin)
# admin.site.register(faq, TranslatableAdmin)
# admin.site.register(Certificate, TranslatableAdmin)
# admin.site.register(video, TranslatableAdmin)
# admin.site.register(Label, TranslatableAdmin)

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['__str__','slug','is_parent']

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['__str__','user','stars','referring_course']


admin.site.register(Label,TranslatableAdmin)
admin.site.register(Testimonial,TranslatableAdmin)
admin.site.register(MCQ,TranslatableAdmin)
admin.site.register(HeaderImg)
# admin.site.register(McqOption,TranslatableAdmin)

@admin.register(McqOption)
class McqOptionAdmin(TranslatableAdmin):
    list_display = ['__str__','correct','title']

    class Meta:
       model = McqOption
# admin.site.register(Certificate)

