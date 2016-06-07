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

from django.utils import timezone

from . import models as m

import datetime

SATURDAY = 5
SUNDAY = 6

def get_working_days(milestone):
    project                 = milestone.project
    holidays, created       = m.BankHolidays.objects.get_or_create(project=project)
    is_ignoring_weekends    = holidays.is_ignoring_weekends
    is_ignoring_days        = holidays.is_ignoring_days
    days_ignored            = holidays.days_ignored

    current_date    = milestone.estimated_start
    days_list       = []

    while current_date <= milestone.estimated_finish:
        if is_ignoring_weekends:
            if current_date.weekday() not in (SATURDAY, SUNDAY):
                days_list.append(current_date)
        elif is_ignoring_days:
            if current_date not in days_ignored:
                days_list.append(current_date)
        else:
            days_list.append(current_date)
        current_date = current_date + datetime.timedelta(days=1)

    return days_list
