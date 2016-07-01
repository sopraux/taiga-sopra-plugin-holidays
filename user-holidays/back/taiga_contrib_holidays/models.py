###
#  Taiga-contrib-holidays is a taiga plugin for manage user holidays.
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
from djorm_pgarray.fields import DateArrayField
from django.utils.translation import ugettext_lazy as _

from .helpers import str_to_date


class UserHolidays(models.Model):
    project = models.ForeignKey("projects.Project", null=True, blank=True,
                                related_name="user_holidays")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              related_name="holidays", verbose_name=_("user"))

    holidays = DateArrayField(blank=True, null=True,
                                      default=[],
                                      verbose_name=_("days taken as holidays"))


    def create(self, *args, **kwargs):
        holidays = map(str_to_date, self.holidays)
        self.holidays = filter(None, holidays)
        super().create(*args, **kwargs)


    def save(self, *args, **kwargs):
        holidays = map(str_to_date, self.holidays)
        self.holidays = filter(None, holidays)
        super().save(*args, **kwargs)
