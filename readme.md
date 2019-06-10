# -> What is this
This project allows you to handle some quantities of money and transfer it to other users. Backend is done with Django and frontend is a Vue app. Both services must be running to use the whole app, but it's also possible to just use Django and consume it's API.

# -> TL;DR
```
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
make run
```
When containers are ready:
```
make init
```
Go to localhost:8080, login with admin/admin and :tada:! Enjoy :)
___
# -> How to install
You can start it with docker (with make aliases) or manually, in any case you will need an environment vars file, so first:
1. Copy env vars file
```
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
2. Edit env vars if needed

## Option 1. Docker
You need docker and docker-compose, then:
1. Build images and start services:
```
make run
```
2. Once Django is running, apply migrations and load initial users to be able to test the app
```
make init
```

## Option 2. Manual
### Django
If you prefer in raw, for Django you need a virtualenv with Python 3 and a Postgres database with a powered user (where you want, local, Docker, RDS...)

1. Go to backend directory
```
cd backend
```
2. In virtualenv install requirements
```
pip install -e .
```
3. Apply migrations
```
python manage.py migrate
```
4. Load initial users
```
python manage.py loaddata fixtures/initial.json
```
5. Start server
```
python manage.py runserver
```

### Vue
And for Vue.js app:

1. Go to frontend directory
```
cd frontend
```
2. Install npm
```
npm install
```
3. Start server
```
npm run serve
```
___
# -> How to use the app
## 1. Info:
- By default Django server is running in port 8000 and Vue in 8080
- On user creation, a new account associated with that user is created automatically with 100€
- Is not possible to remove that account or reassign it
- Is not possible to edit or remove payments once they are done
- You can see payments and accounts in /admin
- You can see API entries in /api Root, but is not supported to create new payments from there, so please don't do it, use Vue, Postman, Curl or whatever
- Entry points:
##### /api/payments/ GET
Will retrieve payments from logged user. Requires content-type and token in headers
##### /api/payments/ POST
Creates a new payment. Requires content-type and token in headers, and a body like:
```json
{
	"amount": 15,
	"receiver": 2
}
```
##### /api/account/ GET
Will retrieve account balance from logged user. Requires content-type and token in headers
##### /api/users/ GET
Will retrieve users list. Requires content-type and token in headers. Used just to fill frontend users selector.

All the functionality can be handled via frontend APP, if want to consume API directly here are few tips:
- Need authentication via Token -> https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
- When using API, Content-type must be "application/json"
- All API entrypoints are prefixed with /api/
- Data retrieved will depend on user who is requesting
- To login, the entrypoint is /api/login. Must provide content-type and body with username and password

Header:
```json
Content-Type:application/json
```
Body:
```json
{
  "username": "admin",
  "password": "admin"
}
```
- Once logged in, to call other points must provide token + content-type in header, for example:

Entrypoint:
```
/api/account
```
Headers:
```json
Authorization:Token 9a67db4d18a2167dbb0d8bb06d3305aac1e6d0eb
Content-Type:application/json
```

And response is:
```json
{
    "id": 1,
    "balance": "100.00"
}
```

## 2. Steps to use Vue.js APP:
### 1. Login in vue app
There are 3 initial users created:
```json
[
    {
        "username": "admin",
        "password": "admin"
    },
    {
        "username": "oriol",
        "password": "oriol"
    },
    {
        "username": "guido",
        "password": "guido"
    },
]
```
When login you see 4 sections:
#### 1. Navigation panel with:
- username (to know who you are)
- payments view (is just this view, not anymore yet)
- logout button
#### 2. Balance:
- you current balance
#### 3. Payments:
- Detailed list of payments done and received
#### 4. Pay:
- Here you can select a user to pay
- An amount to send
- And send it

### 2. Make a transfer
Just fill the simple form with a user, the desired amount and click on Pay. Errors are not handled to be shown but if you inspect the call you can see the error message.
___
# -> Tests
Alias way:
```
make test
```

Normal way (with virtualenv, in backend directory):
```
python manage.py test
```