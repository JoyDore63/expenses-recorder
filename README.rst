expenses_website
================

Problem: 
-------
    Joy and Tony don't know where their cash goes.  Bank statements just show 'cash'. 

Solution: 
--------
    This site will enable them to record their daily cash purchases.

Model:
-----

    Expense
        Description
        Category

    Category
        Description


There are only two users so functionality to add users is not required,
so Django admin can be used to create Joy and Tony.

We need to be able to add categories and expenses, expenses must have a
valid user and category.  The user will be the logged in user and category
will be selectable from the availble ones in the DB.

Developer Build
===============

Check out code then::

    virtualenv --setuptools venv --python=python2.7.6
    . venv/bin/activate
    pip install -e . -r requirements.txt
    ./manage.py rebuild
    ./manage.py runserver

User logins
===========

These two logins are created::

    joy pa55word
    tony pa55word
