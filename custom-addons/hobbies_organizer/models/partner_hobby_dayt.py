from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
# we use datetime and pytz to correctly set start/stop_datetime fields, considering the user's timezone
from datetime import datetime, timedelta
import pytz

class PartnerHobbyDayT(models.Model):
    """Partner Hobby Day Time model. Each entry represents a fixed schedule on the week when a partner practices a hobby."""

    _name = 'hobbies_organizer.partner_hobby_dayt'
    _description = 'Partner Hobby Day Time'
    # _order sets the default order in which the records will be retrieved from the db, in this case,
    # we first sort by day and then by time
    _order = "day_order, time_start"

    # auxiliar structures for days
    _DAYS = [
        ("su", "Sunday"), ("mo", "Monday"), ("tu", "Tuesday"), ("we", "Wednesday"), ("th", "Thursday"), 
        ("fr", "Friday"), ("sa", "Saturday") 
    ]
    _DAYSDICT = dict(_DAYS)
    _ORDERMAP = {"su": 0, "mo": 1, "tu": 2, "we": 3, "th": 4, "fr": 5, "sa": 6}

    name = fields.Char(string="Name", compute="_compute_name", store=True)

    # aggregator=False disables default aggregation when grouping in a list view
    time_start = fields.Float(string="Time Start", required=True, aggregator=False)
    time_end = fields.Float(string="Time End", required=True, aggregator=False)

    # Selection field for day, the group_expand parameter allows us to define how the days will be ordered and shown
    # in case we group by day
    day = fields.Selection(_DAYS, string="Day", required=True, group_expand="_group_expand_day_order")
    # used for order purposes outside of group by day views
    day_order = fields.Integer(compute="_compute_day_order", store=True)

    # the partner and hobby related to this schedule entry
    partner_hobby_id = fields.Many2one(comodel_name="hobbies_organizer.partner_hobby", required=True, ondelete="cascade", string="Schedule")

    # related fields to use in views
    partner_id = fields.Many2one(related="partner_hobby_id.partner_id", store=True, string="Person")
    hobby_id = fields.Many2one(related="partner_hobby_id.hobby_id", store=True, string="Hobby")
    hobby_category_id = fields.Many2one(related="partner_hobby_id.hobby_id.category_id", store=True, string="Category")

    start_datetime = fields.Datetime(string="Start", compute="_compute_start_stop_datetime", store=True)
    stop_datetime = fields.Datetime(string="Stop", compute="_compute_start_stop_datetime", store=True)

    @api.depends("partner_id.short_name", "hobby_id.name")
    def _compute_name(self):
        for rec in self:
            rec.name = rec.hobby_id.name + ", " + rec.partner_id.short_name if rec.hobby_id and rec.partner_id else ""


    @api.depends("day", "time_start", "time_end")
    def _compute_start_stop_datetime(self):
        """ Calculates start/stop_datetime from day, time_start and time_end, in the current week (Sunday to Saturday),
        and in the current user's timezone."""
        weekday_index = self._ORDERMAP  # in odoo, the calendar's first day of the week is Sunday (0), and so on

        for rec in self:
            if not rec.day or rec.time_start is False or rec.time_end is False:
                rec.start_datetime = False
                rec.end_datetime = False
                continue

            # get user's timezone from odoo's context
            tz_name = rec.env.context.get('tz') or (rec.env.user.tz or 'UTC')
            user_tz = pytz.timezone(tz_name)

            # the current datetime in the user's timezone
            now_user = datetime.now(user_tz)

            # week_start is the first day of the current's week (Sunday) at 00:00:00 time
            week_start = now_user - timedelta(days=(now_user.weekday() + 1) % 7)
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

            # day of the week's index
            desired_wd = weekday_index.get(rec.day)
            if desired_wd is None:
                rec.start_datetime = False
                rec.end_datetime = False
                continue
            
            # offset from the week_start to the desired_wd, now we have the exact day of the schedule
            target_date = week_start + timedelta(days=desired_wd)

            # auxiliar function to convert time_float and target_date to the correct datetime
            def float_to_datetime(base_date, time_float):
                hours = int(time_float)
                minutes = int(round((time_float - hours) * 60))
                if minutes == 60:
                    hours += 1
                    minutes = 0
                if hours >= 24:
                    hours -= 24
                    base_date += timedelta(days=1)
                dt_naive = datetime(base_date.year, base_date.month, base_date.day, hours, minutes)
                dt_tz = user_tz.localize(dt_naive)
                dt_utc = dt_tz.astimezone(pytz.UTC)
                return fields.Datetime.to_string(dt_utc)

            # finally, assign the record's start/stop_datetime fields
            rec.start_datetime = float_to_datetime(target_date, rec.time_start)
            rec.stop_datetime = float_to_datetime(target_date, rec.time_end)

    # day_order is an int, depending on day: "su" -> 0, "mo" -> 1, ... , "sa" -> 6
    @api.depends("day")
    def _compute_day_order(self):
        for rec in self:
            rec.day_order = self._ORDERMAP.get(rec.day, 0)

    # the api.model decorator is used when we are not expecting a populated recordset, just use the model's logic
    @api.model
    # group_expand odoo's signature
    def _group_expand_day_order(self, values, domain):
        # we return the groups that exist in our recordset (to not show an empty group), ordered by _DAYS
        existing_days = set(values)
        return [day[0] for day in self._DAYS if day[0] in existing_days]
    
    # constrains
    # not allow time_end < time_start (we assume activity entries are assigned to a single day)
    @api.constrains("time_start", "time_end")
    def _check_time_order(self):
        for rec in self:
            if rec.time_end < rec.time_start:
                raise ValidationError(_("Time's invalid. End time must be greater-equal than start time."))

    # not allow overlapping schedules for the same partner
    @api.constrains("day", "time_start", "time_end", "partner_id")
    def _check_no_overlap(self):
        for rec in self:
            if not rec.partner_id:
                continue
            # search other activities (id != rec.id), for the same partner, in the same day
            overlapping = self.search([
                ("partner_id", "=", rec.partner_id.id),
                ("day", "=", rec.day),
                ("id", "!=", rec.id),
                ("time_start", "<", rec.time_end),  # that start before the current activity ends
                ("time_end", ">", rec.time_start),  # and end after the current activity starts
            ])
            if overlapping:
                raise ValidationError(_(
                    "This activity overlaps with a existing one: %s"
                ) % ", ".join(overlapping.mapped("name")))

    # auxiliar class methods
    @classmethod
    def time_string(cls, time):
        """
        Convierte un float tipo 14.5 en string '14:30'.
        time: número float de horas (puede incluir decimales)
        """
        hours = int(time)
        minutes = round((time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    @classmethod
    def day_string(cls, day):
        return cls._DAYSDICT[day]