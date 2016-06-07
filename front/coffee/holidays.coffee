###
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
#
# File: holidays.coffee
###
debounce = (wait, func) ->
    return _.debounce(func, wait, {leading: true, trailing: false})


class BankHolidaysAdmin
    @.$inject = [
        "$rootScope",
        "$scope",
        "$tgRepo",
        "tgAppMetaService",
        "$tgConfirm",
        "$tgHttp",
    ]

    constructor: (@rootScope, @scope, @repo, @appMetaService, @confirm, @http) ->
        @scope.sectionName = "Bank holidays" # i18n
        @scope.sectionSlug = "bank holidays"

        @scope.$on "project:loaded", =>
            promise = @repo.queryMany("holidays", {project: @scope.projectId})

            promise.then (bank_holidays) =>
                @scope.holidays = {
                    project: @scope.projectId,
                    is_ignoring_weekends: false,
                    is_ignoring_days: false,
                    days_ignored: []
                }
                if bank_holidays.length > 0
                    @scope.holidays = bank_holidays[0]
                #title = "#{@scope.sectionName} - Plugins - #{@scope.project.name}" # i18n
                #description = @scope.project.description
            #@appMetaService.setAll(title, description)



BankHolidaysDirective = ($repo, $confirm, $loading) ->
    link = ($scope, $el, $attrs) ->
        form = $el.find("form").checksley({"onlyOneErrorElement": true})
        submit = debounce 2000, (event) =>
            event.preventDefault()

            return if not form.validate()

            currentLoading = $loading()
                .target(submitButton)
                .start()

            if not $scope.holidays.id
                promise = $repo.create("holidays", $scope.holidays)
                promise.then (data) ->
                    $scope.holidays = data
            else
                promise = $repo.save($scope.holidays)
                promise.then (data) ->
                    $scope.holidays = data

            promise.then (data)->
                currentLoading.finish()
                $confirm.notify("success")

            promise.then null, (data) ->
                currentLoading.finish()
                form.setErrors(data)
                if data._error_message
                    $confirm.notify("error", data._error_message)

        submitButton = $el.find(".submit-button")

        $el.on "submit", "form", submit
        $el.on "click", ".submit-button", submit

    return {link:link}

module = angular.module('taigaContrib.bankholidays', [])

module.controller("ContribBankHolidaysAdminController", BankHolidaysAdmin)
module.directive("contribBankHolidays", ["$tgRepo", "$tgConfirm", "$tgLoading", BankHolidaysDirective])

initBankHolidaysPlugin = ($tgUrls) ->
    $tgUrls.update({
        "holidays": "/holidays"
    })
module.run(["$tgUrls", initBankHolidaysPlugin])
