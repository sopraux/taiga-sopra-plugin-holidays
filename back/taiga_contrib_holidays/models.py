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
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class BankHolidays(models.Model):
    project = models.ForeignKey("projects.Project", null=True, blank=True,
                                related_name="bank_holidays")

    is_ignoring_weekends = models.NullBooleanField(default=False, null=True, blank=True,
                                      verbose_name=_("is ignoring weekends"))
    is_ignoring_days = models.NullBooleanField(default=False, null=True, blank=True,
                                     verbose_name=_("is ignoring specific days"))

    days_ignored = ArrayField(models.DateField(default=None, blank=True, null=True), 
                            blank=True, null=True, default=None, verbose_name=_("days ignored in burndown"))
