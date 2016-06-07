# Copyright (C) 2016 Sopra Steria
# Copyright (C) 2016 David Peris <david.peris92@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from djorm_pgarray.fields import DateTimeArrayField
from django.utils.translation import ugettext_lazy as _


class BankHolidays(models.Model):
    project = models.ForeignKey("projects.Project", null=True, blank=True,
                                related_name="bank_holidays")

    is_ignoring_weekends = models.NullBooleanField(default=False, null=True, blank=True,
                                     verbose_name=_("is ignoring weekends"))
    is_ignoring_days = models.NullBooleanField(default=False, null=True, blank=True,
                                     verbose_name=_("is ignoring specific days"))
    days_ignored = DateTimeArrayField(blank=True, null=True,
                                      default=[],
                                      verbose_name=_("days ignored in burndown"))
