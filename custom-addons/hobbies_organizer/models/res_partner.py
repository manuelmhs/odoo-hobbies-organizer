from odoo import fields, models, api

class ResPartner(models.Model):
    """ res.partner model extension. We include all the necessary app related fields and functions. """

    # using _inherit we can extend the original model, adding fields to the corresponding table and python functionality
    _inherit = "res.partner"

    # boolean used to filter partners, so in our app we only show the ones created inside it
    in_hobbies_organizer = fields.Boolean(default=False)

    # One2many fields, they work only as a reference to a Many2one field that must be defined like inverse_name in the comodel_name
    # useful for views and logic, doesn't modify the underlying model's table
    hobby_ids = fields.One2many(comodel_name="hobbies_organizer.partner_hobby", inverse_name="partner_id", string="Hobbies")
    hobby_dayt_ids = fields.One2many(comodel_name="hobbies_organizer.partner_hobby_dayt", inverse_name="partner_id", string="Hobbies Schedule")

    # related fields, useful to expose a related field from a One2many, Many2one or Many2many relation
    # whereas we can use dot notation to access these related fields directly in python, we cannot do it in xml views,
    # so we need related fields if we wish to show this information in this model's views
    hobby_names = fields.Many2one(related="hobby_ids.hobby_id", store=False)
    hobby_categories = fields.Many2one(related="hobby_ids.hobby_id.category_id", store=False)

    hobbies_summary = fields.Char(string="Hobbies", compute="_compute_hobbies_summary", store=False)

    short_name = fields.Char(string="Short Name", compute="_compute_short_name", store=True)

    # api.depends decorator triggers the compute function if the specified fields change in the db
    @api.depends("name")
    def _compute_short_name(self):
        for record in self:
            l = [word[0] for word in record.name.split()]
            
            record.short_name = ". ".join(l) + "."

    # api.onchange decorator triggers the compute function when the specified fields are modified in the view
    @api.onchange("hobby_ids")
    def _compute_hobbies_summary(self):
        for record in self:
            record.hobbies_summary = ""

            hobbies = record.hobby_ids
            
            for entry in hobbies:
                record.hobbies_summary += f"{entry.hobby_id.name}, "

            record.hobbies_summary = record.hobbies_summary.rstrip(", ")
            record.hobbies_summary = record.hobbies_summary or "No registered hobbies"

    # we override the model's create function, used by odoo when creating a new record, to set in_hobbies_organizer boolean
    # to True if the context contains "in_hobbies_organizer" key
    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get("in_hobbies_organizer"):
            for v in vals:
                v["in_hobbies_organizer"] = True

        return super().create(vals)
