
from app.parts.models import Parts, SectionCarInfo
'''

   Denormalization function, written by junior, took hours to finish

'''

    def denormalize(self):
	#Set min, max prices and count of parts for every section
	SectionCarInfo.objects.all().delete()
        listparts = Parts.objects.filter(section=self)
        for listpart in listparts:
            for car in listpart.parts_by_year.all():
                parts = Parts.objects.filter(section=self, price__gt=0, parts_by_year=car, deletes=0)
                if parts.exists():
                    info = parts.aggregate(Min('price'), Max('price'), Count('id'))
                    price__min = float(info['price__min'])/10
                    price__min = math.ceil(price__min)*10
                    price__max = float(info['price__max'])/10
                    price__max = math.ceil(price__max)*10
                    SectionCarInfo.objects.create(
                        section=self,
                        car=car,
                        price_min=price__min,
                        price_max=price__max,
                        count=info['id__count']
                    )
            reset_queries()
            gc.collect()
        self.denormalize_car()




'''

   After optimization this task takes about 6 min

'''

    def denormalize(self):
	#Set min, max prices and count of parts for every section
	SectionCarInfo.objects.all().delete()
        listparts =  parts_module.parts_model.parts.Parts.objects.filter(section=self)
        cars_in_section = Car.objects.filter(parts__section=self).distinct()
        for car in cars_in_section:
            parts = listparts.filter(parts_by_year=car).order_by('price')
            if parts.exists():
                price__min = parts.first().calculated_price()
                price__max = parts.last().calculated_price()
                SectionCarInfo.objects.create(
                    section=self,
                    car=car,
                    price_min=price__min,
                    price_max=price__max,
                    count=parts.count()
                )
        reset_queries()
        gc.collect()