

'''

   Django Admin model optimization. Spare admin page opened long time (about min) 
	due to large number of queries on big amount of data

'''


class SpareCarInline(SpareInlineMixin, admin.TabularInline):
    model = models.SpareCar

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        ''' optimization because of hard __unicode__ method in ImportCarYear'''
        if db_field.name == 'importcaryear':
            #  override query lookup
            spare = self.get_spare(request)
            kwargs['queryset'] = models.ImportCarYear.objects.filter(spare=spare).prefetch_related('model', 'model__brand').order_by('model__brand', 'model__title', '-start', '-finish')
        return super(SpareCarInline, self).formfield_for_foreignkey(db_field, request, **kwargs)