from django.core.exceptions import ValidationError
from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

class Category(TranslatableModel):
    parent = models.ForeignKey('courses.Category', related_name = "children", on_delete = models.CASCADE, blank = True, null = True) #'self' to indicate a self-reference.
    created_at = models.DateTimeField(auto_now_add = True)
    logo = models.ImageField(upload_to = "catlogo", blank = True, null = True, help_text = 'Optional')
    translations = TranslatedFields(
        title = models.CharField(max_length = 100),
        slug = AutoSlugField(populate_from = 'title', unique = True, blank = True, null = False, editable = True, help_text = 'Leave blank for auto slug.'),
    )

    def __str__(self):
        full_path = [self.title]
        if self.parent:
            if not self.parent.title == self.title:
                k = self.parent
                # this is recursion!
                while k is not None:
                    if k.parent:
                        if k.parent.title == k.title:
                            full_path.append('Invalid Parent')
                            break
                    full_path.append(k.title)
                    k = k.parent
                return ' - > '.join(full_path[::-1]) # reversing the array and joining them with '- > '
            return f"{self.title} (Invalid Parent)"
        return f"{self.title}"

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        verbose_name_plural = "categories"
        # constraints = [
        #     models.UniqueConstraint(fields = ['slug', 'parent'], name = 'unique_parent')
        # ]


    def get_absolute_url(self):
        return reverse('courses:CategoryView', args=[self.slug])

    def post_count(self):
        return self.posts.all().count()

    def is_parent(self):
        if not self.parent:
            return True
        return False



class Label(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length = 100),
        slug = AutoSlugField(populate_from = 'title', unique = True, blank = True, null = False, editable = True, help_text = 'Leave blank for auto slug.'),
        disc = models.BooleanField(default = False, verbose_name = 'Add In Disclaimer'),
    )

    def __str__(self):
        return self.title


class Course(TranslatableModel):
    image = models.ImageField(upload_to = 'course_thumb')
    youtube = models.URLField(max_length = 500, default = '' )
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="courses", null=True)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, related_name = "courses", blank=True)
    hit = models.PositiveIntegerField(default = 0) #This field is for popular posts
    button_text = models.CharField(max_length = 20, default = "Apply Now") #Apply Now and enroll button text
    initial_price = models.IntegerField(default = 0)
    discount = models.IntegerField(default = 0, help_text = "Discount in percent")
    maincourse = models.ManyToManyField(Label, blank = True, related_name = 'posts')
    translations = TranslatedFields(
        title = models.CharField(max_length = 500),
        meta_tags = models.CharField(max_length = 2000, blank = True),
        meta_desc = models.TextField(max_length = 2000, blank = True),
        slug = AutoSlugField(populate_from = 'title', max_length = 500, unique = True, null = False),
        desc = RichTextField(blank = True, null = True),
        why_title = models.CharField(max_length = 500, blank = True),
        why1 = RichTextField(blank = True),
        why2 = RichTextField(blank = True),
        why3 = RichTextField(blank = True),
    )

    def __str__(self):
        return self.title    
        
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.all().values() )
        if self.reviews.count():
            return total / self.reviews.count()
        return 0

    def get_price(self):
        percentage_price = 0
        if self.discount:
            # percentage_price = 100 * float(self.discount)/float(self.initial_price)
            percentage_price = self.initial_price * (self.discount/100)

        price = "{:.2f}".format(self.initial_price - percentage_price)
        return float(price)

    def get_absolute_url(self):
        return reverse('courses:CourseDetailView', args=[self.slug])

    def get_enroll_url(self):
        return reverse('courses:CourseEnrollView', args=[self.slug])

    def get_certificate_url(self):
        url = reverse('courses:GenerateCertificateView')
        return  f"{url}?course={self.slug}&download=true"

    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''


class MCQ(TranslatableModel):
    course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'mcqs')
    serial_number = models.PositiveIntegerField()
    translations = TranslatedFields(
        title = models.CharField(max_length = 500),
    )

    def __str__(self):
        return f"MCQ for {self.course.title}"

class McqOption(TranslatableModel):
    mcq = models.ForeignKey("courses.MCQ", on_delete=models.CASCADE, related_name="options")
    completed = models.ManyToManyField("users.profile", related_name = 'completed_mcqs', blank=True)
    translations = TranslatedFields(
        title = models.CharField(max_length = 300),
    )

    def __str__(self):
        return f"Mcq_Option of {self.course.title}"

class Curriculam(TranslatableModel):
    course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'curriculams')
    video = models.BooleanField(default = True)
    file = models.FileField(upload_to="curriculam_files", blank = True, null = True)
    translations = TranslatedFields(
        title = models.CharField(max_length = 500),
        content = models.TextField(blank = True, null = True),
    )

    def __str__(self):
        return self.title

    def fileURL(self):
        try:
            return self.file.url
        except:
            return '/404'

class video(TranslatableModel):
    course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'videos')
    serial_number = models.IntegerField(null = False)
    url = EmbedVideoField()
    is_preview = models.BooleanField(default = False)

    translations = TranslatedFields(
        title = models.CharField(max_length = 100, null = False),
        desc = models.TextField(blank = True, null = True),
    )

    def __str__(self):
        return self.title

class features(TranslatableModel):
    course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'features')
    translations = TranslatedFields(
        title = models.CharField(max_length = 500),
        content = models.TextField(blank = True, null = True),
    )

class faq(TranslatableModel):
    course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'faqs')
    translations = TranslatedFields(
        title = models.CharField(max_length = 500),
        content = models.TextField(blank = True, null = True),
    )

class Certificate(TranslatableModel):
    course = models.OneToOneField(Course, on_delete = models.CASCADE, related_name="certificate")
    created_at = models.DateTimeField(auto_now_add = True)
    translations = TranslatedFields(
        content = models.TextField(blank = True, null = True),
    )

class Reviews(models.Model):
    referring_course = models.ForeignKey('courses.Course', on_delete = models.CASCADE, related_name = 'reviews')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'reviews')
    stars = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add = True)
    content = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"{self.content[:50]}"

    def validate_unique(self, *args, **kwargs):
        super(Category, self).validate_unique(*args, **kwargs)

        if self.__class__.objects.\
                filter(course=self.course, user=self.user).\
                exists():
            raise ValidationError(
                message='Review already exists.',
                code='unique_together',
            )


class Testimonial(TranslatableModel):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="testimonials/", default="main/default.jpg", null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    dribble = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)

    translations = TranslatedFields(
        content = models.TextField(blank = False, null = False),
    )

    def __str__(self):
        return f"Testimonial of ({self.name})"