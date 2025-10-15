# basic odoo imports to create a new model, define fields in it and use api decorators
from odoo import models, fields, api

# we inherit from odoo's models.Model class to define a new model in our module
class HobbyType(models.Model):
    """ Hobby type/category model. Very simple model, we just define a name for a category.\n
    Could be replaced by a Selection field in hobby model, but this allows the user to define new categories if needed."""

    # _name is used as an external identifier for the model, convention is: "module"."model"
    _name = "hobbies_organizer.hobby_type"
    # _description is a human readable text for the model
    _description = "Hobby Category"

    # the "name" field is usually used by odoo by default to show a record's name when it's referred by other model e.g. in a Many2one field
    name = fields.Char(required=True)