from django.contrib import admin,messages
from .models import Major_transfer,Student_unnormal_change,Grade_downward,Major,Campus,Class,Student,Course,Teacher,Course_sign_up, Student_teacher,Home_information,school_user
from .models import NotGraduateError
from django.urls import reverse
from django.http import HttpResponseRedirect 
class MyModelAdmin(admin.ModelAdmin):
    actions=[]
    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        if queryset.count() == 1:
            message_bit = "1 photoblog entry was"
        else:
            message_bit = "%s photoblog entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"
    
    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except NotGraduateError:
            msg = "Cannot delete none-graduate student"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(object_id,),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except NotGraduateError:
            msg = "Cannot delete none-graduate student"
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)



admin.site.register(Major_transfer)
admin.site.register(Student_unnormal_change)
admin.site.register(Grade_downward)
admin.site.register(Major)
admin.site.register(Campus)
admin.site.register(Class)
admin.site.register(Student,MyModelAdmin)
admin.site.register(Course)
admin.site.register(Teacher,MyModelAdmin)
admin.site.register(Course_sign_up)
admin.site.register(Student_teacher)
admin.site.register(Home_information)
admin.site.register(school_user)


# Register your models here.
