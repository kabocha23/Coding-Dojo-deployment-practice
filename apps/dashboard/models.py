# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        if len(post_data['name']) < 3:
            errors.append("name must be at least 3 characters")
        if len(post_data['username']) < 3:
            errors.append("username must be at least 3 characters")
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")          
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('name must be letters only')
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        if post_data['password'] != post_data['confirm_password']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['name'],
                last_name=post_data['username'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(max_length=255)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.name, self.username, self.email)

class Item(models.Model):
    name = models.CharField(max_length=255)
    item_creator = models.ManyToManyField(User, related_name='wish_list_items')
    def __repr__(self):
        return "<Item object: {}>".format(self.name)