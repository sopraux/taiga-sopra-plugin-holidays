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
from django.utils import timezone

from .models import BankHolidays

import datetime

SATURDAY = 5
SUNDAY = 6

def get_working_days(milestone):
    project                 = milestone.project
    holidays, created       = BankHolidays.objects.get_or_create(project=project)
    is_ignoring_weekends    = holidays.is_ignoring_weekends
    is_ignoring_days        = holidays.is_ignoring_days
    days_ignored            = holidays.days_ignored.all
    print (days_ignored)

    current_date    = milestone.estimated_start
    days_list       = []
    while current_date <= milestone.estimated_finish:
        append = True

        if is_ignoring_weekends and current_date.weekday() in (SATURDAY, SUNDAY):
            append = False
        if is_ignoring_days and current_date in days_ignored:
            append = False
        if append:
            days_list.append(current_date)

        current_date = current_date + datetime.timedelta(days=1)

    return days_list
