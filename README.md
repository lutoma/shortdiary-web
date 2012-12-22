shortdiary
==========

Local (development) Installation
--------------------------------

Install the current version Django and all the dependencies from requirements.txt. (Hint: Use `pip2 install -r requirements.txt` if you're as lazy as me).

Then, execute the following commands:

* `yes no | ./manage.py`
* `./manage.py migrate`

Then, create a super user in the Django shell. Firstly, start it using `./manage.py shell`. Then, execute the following commands:

* `self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')`
* `self.adminuser.save()`
* `self.adminuser.is_staff = True`
* `self.adminuser.save()`

Congratulations, you're done (and can close the shell using `exit()`).

As last step, fire up the local development server using `./manage.py runserver` and point your browser to `http://127.0.0.1:8000`.