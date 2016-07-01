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
from django.apps import AppConfig
from django.conf.urls import include, url


class TaigaContribBankHolidaysAppConfig(AppConfig):
    name = "taiga_contrib_holidays"
    verbose_name = "Taiga contrib holidays App Config"

    def ready(self):
        from taiga.base import routers
        from taiga.urls import urlpatterns
        from .api import BankHolidaysViewSet

        router = routers.DefaultRouter(trailing_slash=False)
        router.register(r"bank_holidays", BankHolidaysViewSet, base_name="bank_holidays")
        urlpatterns.append(url(r'^api/v1/', include(router.urls)))
