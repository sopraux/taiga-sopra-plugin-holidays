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
from taiga.base import filters
from taiga.base import response
from taiga.base.api import ModelCrudViewSet
from taiga.base.decorators import detail_route

from . import models
from . import serializers
from . import permissions


class BankHolidaysViewSet(ModelCrudViewSet):
    model = models.BankHolidays
    serializer_class = serializers.BankHolidaysSerializer
    permission_classes = (permissions.BankHolidaysPermission,)
    filter_backends = (filters.IsProjectAdminFilterBackend,)
    filter_fields = ("project",)

    @detail_route(methods=["POST"])
    def test(self, request, pk=None):
        BankHolidays = self.get_object()

        return response.NoContent()
