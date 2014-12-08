## flinty

liteweite (without the 'gh') service runner

currently can start stop the following services:
- redis-server
- elasticsearch

coming soon:
- open a virtualenv for a repo and start processes defined in a `devProcfile`
    - runserver
    - celery

### running

1. setup your virtualenv (or not)
2. `pip install -r requirements.txt`
3. python main.py