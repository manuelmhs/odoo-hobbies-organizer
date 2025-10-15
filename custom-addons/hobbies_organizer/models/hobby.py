from odoo import models, fields, api

class Hobby(models.Model):
    """ Hobby model. Contains name, category_id (hobby_type), description. """

    _name = 'hobbies_organizer.hobby'
    _description = 'Hobby'

    name = fields.Char(required=True)
    # Many2one fields, works like a foreign key in this table, linked to the comodel (e.g. hobby_type)
    category_id = fields.Many2one(comodel_name="hobbies_organizer.hobby_type", ondelete="set null")
    description = fields.Text()

    # we use computed, not stored fields for display in some views, in this case to show a placeholder if
    # category or description are null or empty
    category_display = fields.Char(store=False, compute="_compute_category_display", string="Category")
    description_display = fields.Char(store=False, compute="_compute_description_display", string="Description")

    # in odoo, the self parameter in a model's function is a recordset of the current model, which can contain
    # 0, 1, or many records
    def _compute_category_display(self):
        # we need to iterate through the recordset to access each record
        for hobby in self:
            # then, we can set fields, execute logic, etc. for each record
            hobby.category_display = hobby.category_id.name or "No category"

    def _compute_description_display(self):
        for hobby in self:
            hobby.description_display = hobby.description or "No description"
