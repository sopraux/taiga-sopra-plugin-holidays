###
#  Taiga-contrib-holidays is a taiga plugin for manage bank holidays.
#
#  Copyright 2016 by Sopra Steria
#  Copyright 2016 by David Peris <david.peris92@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###
from django.db import models
from django.conf import settings
from djorm_pgarray.fields import DateArrayField
from django.utils.translation import ugettext_lazy as _

from .helpers import prepare_dates


class Holidays(models.Model):
    holidays = DateArrayField(
                            blank=True,
                            null=True,
                            default=[],
                            verbose_name=_("days ignored in burndown"))


    class Meta:
        abstract = True
        ordering = ["project"]


    def create(self, *args, **kwargs):
        self.holidays = prepare_dates(self.holidays)
        super().create(*args, **kwargs)


    def save(self, *args, **kwargs):
        self.holidays = prepare_dates(self.holidays)
        super().save(*args, **kwargs)




class BankHolidays(Holidays):
    project = models.OneToOneField("projects.Project",
                                null=True,
                                blank=True,
                                related_name="bank_holidays",
                                verbose_name=_("project"))

    is_ignoring_weekends = models.NullBooleanField(
                                    default=False,
                                    null=True,
                                    blank=True,
                                    verbose_name=_("is ignoring weekends"))

    is_ignoring_days = models.NullBooleanField(
                                    default=False,
                                    null=True,
                                    blank=True,
                                    verbose_name=_("is ignoring specific days"))



    class Meta(Holidays.Meta):
            verbose_name = "bank holidays"
            verbose_name_plural = "bank holidays"



class UserHolidays(Holidays):
    project = models.ForeignKey("projects.Project",
                                null=True,
                                blank=True,
                                related_name="user_holidays",
                                verbose_name=_("project"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            null=True,
                            blank=True,
                            related_name="user_holidays",
                            verbose_name=_("user"))

    max_days = models.PositiveIntegerField( blank=True,
                                            null=True,
                                            default=23,
                                            verbose_name=_("maximum days of holidays per year"))


    class Meta(Holidays.Meta):
            verbose_name = "user holidays"
            verbose_name_plural = "user holidays"
