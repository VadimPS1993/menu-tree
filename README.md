### Запуск проекта
Для Windows:
```shell
git clone https://github.com/VadimPS1993/menu-tree.git
cd menu-tree
python -m venv djvenv
/Scripts/activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```
Для Linux:
```shell
git clone https://github.com/VadimPS1993/menu-tree.git
cd menu-tree
python3 -m venv djvenv
source venv/bin/activat
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```
Для корректной работы приложения необходимо:

*создать суперпользователя
```shell
python manage.py createsuperuser
```
*создать меню и его элементы через административную панель.
Запустить сервер разработки
```shell
python manage.py runserver
```