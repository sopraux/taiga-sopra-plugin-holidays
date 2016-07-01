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
            promise = @repo.queryMany("bank_holidays", {project: @scope.projectId})

            promise.then (bank_holidays) =>
                @scope.bank_holidays = {
                    project: @scope.projectId,
                    is_ignoring_weekends: false,
                    is_ignoring_days: false,
                    holidays: []
                }
                if bank_holidays.length > 0
                    @scope.bank_holidays = bank_holidays[0]

                day_picker = $('#day_picker')

                day_picker.multiDatesPicker({
                    firstDay: 1,
                    dateFormat: 'yy-mm-dd'
                })

                if @scope.bank_holidays.is_ignoring_weekends
                    day_picker.multiDatesPicker({ beforeShowDay: $.datepicker.noWeekends })


                holidays = @array_str_to_date @scope.bank_holidays.holidays

                if holidays? and holidays.length > 0
                    day_picker.multiDatesPicker 'addDates', holidays


    array_str_to_date: (array) ->
        if array? and array.length > 0
            result = array.substr(1, array.length-2).split('"').join('')
            result = result.split(',')
            result = result.map( (el) -> new Date(el.trim()) )



BankHolidaysDirective = ($repo, $confirm, $loading) ->
    link = ($scope, $el, $attrs) ->
        $scope.changeWeekends = () =>
            if $scope.bank_holidays.is_ignoring_weekends
                day_picker.multiDatesPicker({ beforeShowDay: $.datepicker.noWeekends })
            else
                day_picker.multiDatesPicker({ beforeShowDay: () -> [true] })

            return false


        save = debounce 2000, (event) =>
            event.preventDefault()

            currentLoading = $loading()
                .target(submitButton)
                .start()

            holidays = day_picker.multiDatesPicker 'getDates', 'object'
            holidays = holidays.map( (el) -> $.datepicker.formatDate 'dd-mm-yy', el )
            $scope.bank_holidays.holidays = holidays.filter( (date) -> !isNaN(parseInt(date.split('-'))) )

            if not $scope.bank_holidays.id
                promise = $repo.create("bank_holidays", $scope.bank_holidays)
                promise.then (data) ->
                    $scope.bank_holidays = data
            else
                promise = $repo.save($scope.bank_holidays)
                promise.then (data) ->
                    $scope.bank_holidays = data

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
        "bank_holidays": "/bank_holidays"
    })
module.run(["$tgUrls", initBankHolidaysPlugin])
