from odoo import fields, models, api, _
# ValidationError can be used to show custom errors to the user
from odoo.exceptions import ValidationError

class PartnerHobby(models.Model):
    """ Partner Hobby model. Works as the intermediate table between res.partner and hobby models, with additional embedded data.\n
    Could have used a Many2many odoo field in place of this model, but this allows us to insert data for each partner-hobby relation. """

    _name = 'hobbies_organizer.partner_hobby'
    _description = 'Partner Hobby'

    # this is a simple intermediate table, with indexes to partner and hobby tables (models)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True, ondelete="cascade")
    hobby_id = fields.Many2one(comodel_name="hobbies_organizer.hobby", required=True, ondelete="cascade")

    # we add the schedule, or day time, related to this entry, as well as a summary and related field for the hobby categories
    partner_hobby_dayt_ids = fields.One2many(comodel_name="hobbies_organizer.partner_hobby_dayt", inverse_name="partner_hobby_id", string="Schedule")

    schedule_summary = fields.Char(string="Schedule", compute="_compute_schedule_summary", store=False)

    hobby_category_id = fields.Many2one(string="Category", related="hobby_id.category_id", store=True)

    # we compute the schedule summary to show in the xml views
    @api.onchange("partner_hobby_dayt_ids")
    def _compute_schedule_summary(self):
        for record in self:
            record.schedule_summary = ""

            schedule = record.partner_hobby_dayt_ids
            
            for dayt in schedule:
                # here we use PartnerHobbyDayT model methods like day/time_string
                day = dayt.day_string(dayt.day)
                hour_start = dayt.time_string(dayt.time_start)
                hour_end = dayt.time_string(dayt.time_end)

                record.schedule_summary += f"{day} {hour_start}-{hour_end}, "

            record.schedule_summary = record.schedule_summary.rstrip(", ")
            record.schedule_summary = record.schedule_summary or "No schedule specified"

    # api.constrains decorator enables us to validate information when there's a change on the specified fields
    @api.constrains("partner_id", "hobby_id")
    def _check_unique_hobby(self):
        # we only allow each hobby to be registered once for each partner
        for rec in self:
            if not rec.partner_id or not rec.hobby_id:
                continue
            exists = self.search([
                ("partner_id", "=", rec.partner_id.id),
                ("hobby_id", "=", rec.hobby_id.id),
                ("id", "!=", rec.id),
            ])
            if exists:
                raise ValidationError(_("This hobby is already registered for this person."))
