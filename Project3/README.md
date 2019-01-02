# Project 3 - PizzaHub

A website using Django to implement an online ordering site for the [Pinocchio's Pizza & Subs](http://www.pinocchiospizza.net/menu.html) restaurant in Cambridge, MA (renamed here as PizzaHub...because word-play).

## Main Files
### orders folder
The main files for the site's backend are:
- **models.py:** defines the models for menu items, order items (menu items with add on's/extras, etc), and shopping cart.
- **views.py:** defines the views for the different pages, including what database objects/queries to make.
- **urls.py:** corresponding url patterns defined here.
- **admin.py** administrative view of menu items and shopping carts (including those in-process and complete orders placed)

#### templates folder
The front-end menu display, order item forms, shopping cart page, and user login/registration all live here.

## Personal Touch: Order Confirmation Email
As can be seen in orders/views.py's check_out view, an email is sent to the user after they've placed an order. The email includes order confirmation number and order items displayed in html (see orders/templates/orders/order_conf.html).

The following settings had to be added to pizza/settings.py (with environment variables defined where appropriate):
```
ADMINS = (
        ('FULLNAME', os.getenv("SERVER_NO_REPLY_EMAIL")),
)

MANAGERS = ADMINS
MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
TEST_EMAIL_BACKEND_RECIPIENTS = ADMINS

FROM_EMAIL = ADMINS[0][1]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = FROM_EMAIL
EMAIL_HOST_PASSWORD = os.getenv("SERVER_NO_REPLY_EMAILPW")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

This was done mainly because I'm using my gmail to test the email sending features.

**--IMPORTANT--**
With the above in mind, it is only possible to send emails from your Gmail account by allowing less secure apps. This permission can be set here: https://myaccount.google.com/lesssecureapps

## Supplemental Files
import.py and menu.csv were used to import the restaurant's existing menu into the database using Django's shell interface (`exec(open('import.py').read())`)

## Technical References
The Django tutorials were incredibly helpful for getting situated before starting the project: https://docs.djangoproject.com/en/2.1/intro/tutorial01/. My follow-along files are in the django-tutorial folder.

AJAX with CSRF tokens: Certain features of the website use AJAX requests, which can be tricky to configure with Django's CSRF token requirements. The following code is included in orders/base.html to retrieve the csrf token and have any other webpage inheriting base.html to access the csrf token (using the JavaScript Cookie Library):
```
<script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
<script type="text/javascript">
  // csrftoken for AJAX requests using JS-Cookies
  var csrftoken = Cookies.get('csrftoken');
</script>
```
Requests are then appended with csrf token in javascript:
```
request.setRequestHeader("X-CSRFToken", csrftoken);
```
Full documentation of how this works is in Django's documentation (https://docs.djangoproject.com/en/2.1/ref/csrf/#ajax

Modals were used for the OrderItem form display. The w3schools modal reference was incredibly helpful: https://www.w3schools.com/howto/howto_css_modals.asp
