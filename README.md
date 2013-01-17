shortdiary
==========

Local (development) Installation
--------------------------------

Install the current version Django and all the dependencies from requirements.txt. (Hint: Use `pip2 install -r requirements.txt` if you're as lazy as me).

Then, execute the following commands:

* `yes no | ./manage.py syncdb`
* `./manage.py migrate`

Next, create an admin user
* `./manage.py createsuperuser`

Congratulations, you're done.

As last step, fire up the local development server using `./manage.py runserver` and point your browser to `http://127.0.0.1:8000`.
