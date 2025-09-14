# 代码生成时间: 2025-09-14 12:36:23
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Model Module
This module contains the data models used by the Falcon application.
"""

from falcon import HTTPError
from peewee import Model, CharField, IntegerField, SqliteDatabase
from playhouse.shortcuts import model_to_dict

# Define the database connection
db = SqliteDatabase('app.db', auto_create_tables=True)


class BaseModel(Model):
    """Base Model that provides common functionality for all models."""
    class Meta:
        database = db


    @staticmethod
    def model_to_dict(model_instance):
        """Converts a model instance to a dictionary."""
        return model_to_dict(model_instance)



class User(BaseModel):
    """User data model."""
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        """Saves the model instance to the database."""
        try:
            super(User, self).save(*args, **kwargs)
        except Exception as e:
            raise HTTPError(f"Failed to save user: {e}", 500)

    def delete_instance(self, *args, **kwargs):
        """Deletes the model instance from the database."""
        try:
            super(User, self).delete_instance(*args, **kwargs)
        except Exception as e:
            raise HTTPError(f"Failed to delete user: {e}", 500)


# Initialize the database and create tables if they don't exist
db.connect()
db.create_tables([User])


# Close the database connection
db.close()
