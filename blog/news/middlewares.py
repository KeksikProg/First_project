def page_context_processor(request):
	context = {}
	context['page'] = ''
	context['all'] = ''
	if 'page' in request.GET:
		page = request.GET['page']
		if page != '1':
			context['all'] = '?page=' + page
	return context