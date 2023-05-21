# from django.shortcuts import render
from django.views.generic import ListView, DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import News
from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import NewsFilter # импортируем недавно написанный фильтр
 
 
class NewsList(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = News.objects.order_by('-id')

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        context['value1'] = None # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
 
class NewsDetail(DetailView):
    model = News # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'detail.html' # название шаблона будет product.html
    context_object_name = 'detail' # название объекта  


class News(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-name']
    paginate_by = 1 # поставим постраничный вывод в один элемент
 
 
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context