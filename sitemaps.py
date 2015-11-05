...

class PartsWithModelSitemap(MarkSectionSitemap):
    '''
        Parts connected with models urls list 
    '''
    priority = 0.4

    def items_iterator(self, csv=False, category=None):
        for part in queryset_iterator(Parts.objects.all().prefetch_related('parts_by_year', 'parts_by_year__model', 'section').select_related('section__slug')):
            models = [c.model for c in part.parts_by_year.all()]
            for model in models:
                if csv:
                    title = u'%s для %s (%s)' % (part.section, model, part.article)
                    yield self.get_csv_info(reverse('parts:product_detail', kwargs={
                        'slug': part.section.slug,
                        'slug_year': model.slug,
                        'article_slug': part.article_slug}), part.updated_at, title=title, category=category)
                else:
                    yield self.get_info(reverse('parts:product_detail', kwargs={
                        'slug': part.section.slug,
                        'slug_year': model.slug,
                        'article_slug': part.article_slug}), part.updated_at)

...

 
def commit_manually(fn=None):
    '''
	Manual commit decorator for django 1.8 
    '''
    def _commit_manually(*args, **kwargs):
        transaction.set_autocommit(False)
        res = fn(*args, **kwargs)
        transaction.commit()
        transaction.set_autocommit(True)
        return res
    return _commit_manually

@commit_manually
def quick_db_file_sitemap_generator(sitemaps, filename):
    stmp_cnt = 0
    stmp_len = len(sitemaps)
    for key, SitemapClass in sitemaps.iteritems():
        sitemap = SitemapClass()
        transcounter = 0
        stmp_cnt += 1
        set_status('%s (%d/%d)' % (key, stmp_cnt, stmp_len))
        for item in sitemap.items_iterator():
            sm_item = SitemapItem(**item)
            sm_item.save()
            transcounter += 1
            if (transcounter == 1000):
                transaction.commit()
                transcounter = 0
        gc.collect()
    return db_sitemap_to_file(filename)

...