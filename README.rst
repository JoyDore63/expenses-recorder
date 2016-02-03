expenses_website

Problem: Joy and Tony don't know where their cash goes.  Bank statements 
    just show 'cash'. 

Solution: This site will enable them to record their daily cash purchases.

Model:

Expense
    User
    Description
    Category

Category
    Name

User
    Name


There are only two users so functionality to add users is not required,
    so Django admin can be used to create Joy and Tony

We need to be able to add categories and expenses, expenses must have a
valid user and category so user should be able to select from the
availble options.  Defaults of those should be the last used values.
