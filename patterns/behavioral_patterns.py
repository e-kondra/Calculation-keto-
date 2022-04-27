# поведенческий паттерн - Шаблонный метод
import jsonpickle as jsonpickle

from templator import render


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        # print(f'queryset= {queryset}')
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    queryset = {}
    template_name = 'create.html'
    template_name_post = 'create_post.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def get_template_post(self):
        return self.template_name_post

    def render_template_with_context_post(self): # переопределяю чтобы по результатм перейти на другую страницу
        template_name_post = self.get_template_post()
        context = self.get_context_data()
        return '200 OK', render(template_name_post, **context)

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context_post()
        else:
            return super().__call__(request)


# паттерн наблюдатель
class Observer:
    def update(self, subject):
        pass

class Subject:
    def __init__(self):
        self.observers = []


    def attach(self, observer):
        observer._subject = self
        self.observers.append(observer)

    def notify(self):
        for item in self.observers:
            item.update(self)


class DBWriter(Observer):
    def update(self, subject):
        print(f'Добавлен расчет с id= {subject.calc.id}')

# Создание api
class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)