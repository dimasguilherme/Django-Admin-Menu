from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

site = admin.site

def applist(request):
	app_dict = {}
	user = request.user
	for model, model_admin in site._registry.items():
		app_label = model._meta.app_label
		has_module_perms = user.has_module_perms(app_label)
		
		if has_module_perms:
			perms = model_admin.get_model_perms(request)
			
			if True in perms.values():
				model_dict = {
					'name': capfirst(model._meta.verbose_name_plural),
					'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
					'perms': perms,
				}
				if app_label in app_dict:
					app_dict[app_label]['models'].append(model_dict)
				else:
					app_dict[app_label] = {
						'name': app_label.title(),
						'app_url': '/admin/' + app_label + '/',
						'has_module_perms': has_module_perms,
						'models': [model_dict],
					}
					
	app_list = app_dict.values()
	app_list.sort(lambda x, y: cmp(x['name'], y['name']))
	return {'adm_app_list': app_list}
