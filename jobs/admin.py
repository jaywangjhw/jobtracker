from django.contrib import admin
import jobs.models as jobs_models


admin.site.register(jobs_models.Position)
admin.site.register(jobs_models.Company)
admin.site.register(jobs_models.Account)
admin.site.register(jobs_models.Application)
admin.site.register(jobs_models.Interview)
admin.site.register(jobs_models.Assessment)
