# E-commerce project
This project has been implemented the Inventory app what maintain the data that is needed to support online retail sales and stock inventory management, with the promotion component and search.  
Web application integrating Django, DRF, PostgreSQL, Celery (with Celery Beat, Redis, Flower), Docker, PyTest, ElasticSearch.

## Setup
1. Download code and open in code editor.
2. Create and activate Virtual Environment.
3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Install Docker desktop.

5. Start the new containers:

```
docker compose up -d
```

6. Load the fixtures into the database:

```
python manage.py demo-fixtures
```

9. Start the server:

```
python manage.py runserver
```
