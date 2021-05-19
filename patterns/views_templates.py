"""
    Module contains templates for different types of views, such as: TemplateView, ListView and CreateView.
"""
from zorro_framework.template_reader import render
from .logger import Logger

logger = Logger('views_templates')


class TemplateView:
    """
    Base template for a view
    """
    template_name = ''

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def set_template_name(self, new_template_name):
        self.template_name = new_template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        logger.log(f'got template: {template_name} and context: {context}')
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = ''
    context_object_name = ''

    def get_queryset(self):
        logger.log(f"Received a queryset: {self.queryset}")
        return self.queryset

    def get_context_object_name(self):
        logger.log(f"Received a context object name: {self.context_object_name}")
        return self.context_object_name

    def get_context_data(self):
        context_object_name = self.get_context_object_name()
        queryset = self.get_queryset()
        context = {context_object_name: queryset}
        logger.log(f"Got a context: {context}")
        return context


class CreateView(TemplateView):
    template_name = ''

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return self.render_template_with_context()

        else:
            return super().__call__(request)


class UpdateView(TemplateView):
    template_name = ''

    @staticmethod
    def get_request_data(request):
        return request['data']

    def update_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.update_object(data)
            return self.render_template_with_context()

        else:
            return super().__call__(request)
