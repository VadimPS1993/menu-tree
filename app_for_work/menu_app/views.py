from django.shortcuts import render

# Представление для главной страницы
def index_view(request):
    return render(request, 'menu_app/index.html')

# Представление для других страниц
def about_view(request):
    return render(request, 'menu_app/about.html')

def services_view(request):
    return render(request, 'menu_app/services.html')

def consulting_view(request):
    return render(request, 'menu_app/consulting.html')
