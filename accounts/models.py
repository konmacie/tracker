from django.db import models
from django.contrib.auth.models import User

# Make User.email unique and required on db level
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
