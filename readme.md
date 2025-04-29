## Steps to run 

- run ``pip install -r requirements.txt``
- run ``python3 main.py`` or ``flask --app main.py run``

## some considerations 

- For production I would use flask db migrate/upgrade, here I call db.create_all() to keep the demo self-contained.
- "JWT_COOKIE_SECURE" would be set to True in production
- primary key for all tables would be uuid in prod as opposed to using integer (integers can easily overflow in real world application and prevents sequential id attack)
- Secrets would be in a .env file 
- db is included but for production I would probably use postgres