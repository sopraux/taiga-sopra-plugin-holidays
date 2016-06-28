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

                day_picker = $('#day_picker')

                day_picker.multiDatesPicker({
                    firstDay: 1,
                    dateFormat: 'yy-mm-dd'
                })

                if @scope.holidays.is_ignoring_weekends
                    day_picker.multiDatesPicker({ beforeShowDay: $.datepicker.noWeekends })


                days_ignored = @array_str_to_date @scope.holidays.days_ignored

                if days_ignored.length > 0
                    day_picker.multiDatesPicker 'addDates', days_ignored


    array_str_to_date: (array) ->
        result = array.substr(1, array.length-2).split('"').join('')
        result = result.split(',')
        result = result.map( (el) -> new Date(el.trim()) )



BankHolidaysDirective = ($repo, $confirm, $loading) ->
    link = ($scope, $el, $attrs) ->
        $scope.changeWeekends = () =>
            if $scope.holidays.is_ignoring_weekends
                day_picker.multiDatesPicker({ beforeShowDay: $.datepicker.noWeekends })
            else
                day_picker.multiDatesPicker({ beforeShowDay: () -> [true] })

            return false


        save = debounce 2000, (event) =>
            event.preventDefault()

            currentLoading = $loading()
                .target(submitButton)
                .start()

            days_ignored = day_picker.multiDatesPicker 'getDates', 'object'
            days_ignored = days_ignored.map( (el) -> $.datepicker.formatDate 'dd-mm-yy', el )
            $scope.holidays.days_ignored = days_ignored.filter( (date) -> !isNaN(date) )

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
                if data._error_message
                    $confirm.notify("error", data._error_message)


        reset = debounce 2000, (event) =>
            event.preventDefault()
            day_picker.multiDatesPicker 'resetDates', 'picked'



        submitButton = $el.find(".save-button")

        day_picker = $('#day_picker')

        $el.on "click", ".save-button", save

        $el.on "click", "#reset_picker", reset


    return {link:link}


module = angular.module('taigaContrib.bankholidays', [])

module.controller("ContribBankHolidaysAdminController", BankHolidaysAdmin)
module.directive("contribBankHolidays", ["$tgRepo", "$tgConfirm", "$tgLoading", BankHolidaysDirective])

initBankHolidaysPlugin = ($tgUrls) ->
    $tgUrls.update({
        "holidays": "/holidays"
    })
module.run(["$tgUrls", initBankHolidaysPlugin])
