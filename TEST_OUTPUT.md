# Test Output

This file can be used to record test results, validation notes, and CI evidence for the project.

## 1. Install Dependencies

PS B:\WareNexa> pip install -r requirements.txt
Requirement already satisfied: Django==4.2.30 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from -r requirements.txt (line 1)) (4.2.30)
Requirement already satisfied: psycopg2-binary==2.9.12 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from -r requirements.txt (line 2)) (2.9.12)
Requirement already satisfied: gunicorn==23.0.0 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from -r requirements.txt (line 3)) (23.0.0)
Requirement already satisfied: whitenoise==6.9.0 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from -r requirements.txt (line 4)) (6.9.0)
Requirement already satisfied: asgiref<4,>=3.6.0 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from Django==4.2.30->-r requirements.txt (line 1)) (3.11.1)
Requirement already satisfied: sqlparse>=0.3.1 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from Django==4.2.30->-r requirements.txt (line 1)) (0.5.5)
Requirement already satisfied: tzdata in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from Django==4.2.30->-r requirements.txt (line 1)) (2025.3)
Requirement already satisfied: packaging in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from gunicorn==23.0.0->-r requirements.txt (line 3)) (25.0)
Requirement already satisfied: typing_extensions>=4 in c:\users\91952\appdata\local\programs\python\python310\lib\site-packages (from asgiref<4,>=3.6.0->Django==4.2.30->-r requirements.txt (line 1)) (4.15.0)

## 2. Database Migration

PS B:\WareNexa> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, boxes, contenttypes, orders, products, recommendations, sessions
Running migrations:
  No migrations to apply.

## 3. Seed Demo Data

PS B:\WareNexa> python manage.py seed_demo_data
Loaded 15 products, 6 boxes, and 10 sample orders.

## 4. Create Superuser
PS B:\WareNexa> python manage.py createsuperuser
Username (leave blank to use '91952'): bhaktibh
Email address: bhakti@gmail.com
Password: *****
Password (again): ***** 
Superuser created successfully.

## 5. Run Tests

PS B:\WareNexa> python manage.py test
Found 36 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......INFO 2026-06-27 01:32:21,676 orders.services.order_service Packing confirmed for order SVC-ORD-1
.INFO 2026-06-27 01:32:21,690 orders.services.order_service Packing confirmed for order SVC-ORD-1
.....C:\Users\91952\AppData\Local\Programs\Python\Python310\lib\site-packages\django\core\handlers\base.py:61: UserWarning: No directory at: B:\WareNexa\staticfiles\
  mw_instance = middleware(adapted_handler)
INFO 2026-06-27 01:32:22,094 orders.services.order_service Packing confirmed for order VIEW-ORD-1
...INFO 2026-06-27 01:32:22,839 recommendations.services.recommendation_service Recommended box VIEW-BOX for order VIEW-ORD-1
....Loaded 15 products, 6 boxes, and 10 sample orders.
INFO 2026-06-27 01:32:22,908 recommendations.services.recommendation_service Recommended box BX-S01 for order ORD001
INFO 2026-06-27 01:32:22,911 recommendations.services.recommendation_service Recommended box BX-S01 for order ORD002
INFO 2026-06-27 01:32:22,915 recommendations.services.recommendation_service Recommended box BX-L01 for order ORD003
INFO 2026-06-27 01:32:22,921 recommendations.services.recommendation_service Recommended box BX-L01 for order ORD004
INFO 2026-06-27 01:32:22,926 recommendations.services.recommendation_service Recommended box BX-M01 for order ORD005
INFO 2026-06-27 01:32:22,927 recommendations.services.recommendation_service Recommended box BX-M01 for order ORD006
INFO 2026-06-27 01:32:22,927 recommendations.services.recommendation_service Recommended box BX-M01 for order ORD007
INFO 2026-06-27 01:32:22,935 recommendations.services.recommendation_service Recommended box BX-XL01 for order ORD008
INFO 2026-06-27 01:32:22,941 recommendations.services.recommendation_service Recommended box BX-XL01 for order ORD009
INFO 2026-06-27 01:32:22,944 recommendations.services.recommendation_service Recommended box BX-XL01 for order ORD010
.INFO 2026-06-27 01:32:22,950 recommendations.services.recommendation_service Recommended box BX-XL01 for order ORD010
....WARNING 2026-06-27 01:32:22,977 recommendations.services.recommendation_service No suitable box for order ORD-HEAVY (weight=15.000, envelope=(Decimal('10.00'), Decimal('10.00'), Decimal('10.00')))
.INFO 2026-06-27 01:32:22,983 recommendations.services.recommendation_service Recommended box BOX-SM for order ORD-2001
...........
----------------------------------------------------------------------
Ran 36 tests in 1.324s

OK
Destroying test database for alias 'default'...

## 6. Run

PS B:\WareNexa> python manage.py runserver
INFO 2026-06-27 01:34:43,635 django.utils.autoreload Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 27, 2026 - 01:34:43
Django version 4.2.30, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.