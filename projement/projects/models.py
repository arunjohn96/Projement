from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError 

class Company(models.Model):

    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


def validate_hours(value):
    if value >=0 and value <10000:
        return value
    else:
        raise ValidationError("This field accepts values between 0 and 10000 ")


class Project(models.Model):

    company = models.ForeignKey('projects.Company', on_delete=models.PROTECT, related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.DecimalField('Estimated design hours', max_digits=7, decimal_places=2, validators =[validate_hours])
    actual_design = models.DecimalField('Actual design hours', default=0, max_digits=7, decimal_places=2, validators =[validate_hours])

    estimated_development = models.DecimalField('Estimated development hours', max_digits=7, decimal_places=2, validators =[validate_hours])
    actual_development = models.DecimalField('Actual development hours', default=0, max_digits=7, decimal_places=2, validators =[validate_hours])

    estimated_testing = models.DecimalField('Estimated testing hours', max_digits=7, decimal_places=2, validators =[validate_hours])
    actual_testing = models.DecimalField('Actual testing hours', default=0, max_digits=7, decimal_places=2, validators =[validate_hours])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk, 'slug': slugify(self.title)})

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development + self.actual_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours
