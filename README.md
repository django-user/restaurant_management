# restaurant_management
This application helps a company to make a decision on lunch place. Each restaurant uploads menus using the system every day over API and employees vote for the menu before leaving for lunch. 

###Development
####Following steps to setup:
    - clone the repository
    - Create a virtualenv using Python 3 and install dependencies.
    pip install -r requirements.txt
    
* Set up db (change database name):

```python manage.py migrate```

* Testing
Run tests:

```python manage.py test```

###Run source with docker
```
- docker-compose up --build
- docker-compose up 
- docker-compose run web python restaurant_management/manage.py migrate
- docker-compose run web python restaurant_management/manage.py createsuperuser
- docker-compose run web python restaurant_management/manage.py test restaurants
```

###API Details
####Authentication
>/auth/login/ (POST)
>- username
>- password
####Creating restaurant and employee
>/auth/registration/ (POST)
>- username
>- password1
>- password2
>- email
>- is_restaurant
>>Optional verification:/auth/registration/verify-email/ (POST)
>>- key
####Uploading menu for restaurant 
> /restaurant/menus/ (POST)
>- name
####Getting current day menu
> /restaurant/restaurant-menus/ (GET)
####Voting for restaurant menu
> /restaurant/restaurant-menus/ (POST)
>- menu_id
####Getting results for the current day
> Execute a django management command to update a result in the database.
> Admin can check the result on admin panel.
>
> Command: python manage.py updatewinnerrestaurant
>
> API to get a winning restaurant is
>
> /restaurant/winning-restaurant/ (GET)
####Logout 
> /auth/logout/ (GET)

####Forgot password
>/auth/password/reset/ (POST)
>- email
>
>/auth/password/reset/confirm/ (POST)
>- uid
>- token
>- new_password1
>- new_password2

####Change password
>/auth/password/change/ (POST)
>- new_password1
>- new_password2
>- old_password

#####ToDo
- Detailed menu
