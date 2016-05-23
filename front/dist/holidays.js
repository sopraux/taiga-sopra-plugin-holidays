angular.module("templates").run(["$templateCache", function($templateCache) {$templateCache.put("/plugins/holidays/holidays.html","\n<div contrib-bank-holidays=\"contrib-bank-holidays\" ng-controller=\"ContribBankHolidaysAdminController as ctrl\">\n  <header>\n    <h1><span class=\"project-name\">{{::project.name}}</span><span class=\"green\">{{::sectionName}}</span></h1>\n  </header>\n  <form>\n    <fieldset>\n      <div class=\"check-item\"><span>Ignore weekends</span>\n        <div class=\"check\">\n          <input type=\"checkbox\" name=\"ignore_weekends\" ng-model=\"holidays.is_ignoring_weekends\"/>\n          <div></div><span translate=\"COMMON.YES\" class=\"check-text check-yes\"></span><span translate=\"COMMON.NO\" class=\"check-text check-no\"></span>\n        </div>\n      </div>\n    </fieldset>\n    <!--/fieldset\n    h2 Ignore specific days\n    div.check-item\n        span Ignore selected days\n        div.check\n            input(type=\"checkbox\" name=\"ignore_days\" ng-model=\"holidays.is_ignoring_days\")\n            div\n            span.check-text.check-yes(translate=\"COMMON.YES\")\n            span.check-text.check-no(translate=\"COMMON.NO\")\n    \n    // Date picker\n    \n    \n    -->\n    <button type=\"submit\" title=\"{{\'COMMON.SAVE\' | translate}}\" translate=\"COMMON.SAVE\" class=\"button-green submit-button\"></button>\n    <tg-svg svg-icon=\"icon-question\"></tg-svg><span>Do you need help? Check out our support page!</span>\n  </form>\n</div>");}]);

/*
 * Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
 * Copyright (C) 2014-2016 Jesús Espino Garcia <jespinog@gmail.com>
 * Copyright (C) 2014-2016 David Barragán Merino <bameda@dbarragan.com>
 * Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
 * Copyright (C) 2014-2016 Juan Francisco Alcántara <juanfran.alcantara@kaleidos.net>
 * Copyright (C) 2014-2016 Xavi Julian <xavier.julian@kaleidos.net>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * File: slack.coffee
 */

(function() {
  var BankHolidaysAdmin, BankHolidaysDirective, debounce, initBankHolidaysPlugin, module;

  debounce = function(wait, func) {
    return _.debounce(func, wait, {
      leading: true,
      trailing: false
    });
  };

  BankHolidaysAdmin = (function() {
    BankHolidaysAdmin.$inject = ["$rootScope", "$scope", "$tgRepo", "tgAppMetaService", "$tgConfirm", "$tgHttp"];

    function BankHolidaysAdmin(rootScope, scope, repo, appMetaService, confirm, http) {
      this.rootScope = rootScope;
      this.scope = scope;
      this.repo = repo;
      this.appMetaService = appMetaService;
      this.confirm = confirm;
      this.http = http;
      this.scope.sectionName = "Bank holidays";
      this.scope.sectionSlug = "bank holidays";
      this.scope.$on("project:loaded", (function(_this) {
        return function() {
          var promise;
          promise = _this.repo.queryMany("holidays", {
            project: _this.scope.projectId
          });
          return promise.then(function(bank_holidays) {
            _this.scope.holidays = {
              project: _this.scope.projectId,
              is_ignoring_weekends: false,
              is_ignoring_days: false,
              days_ignored: []
            };
            if (bank_holidays.length > 0) {
              return _this.scope.holidays = bank_holidays[0];
            }
          });
        };
      })(this));
    }

    return BankHolidaysAdmin;

  })();

  BankHolidaysDirective = function($repo, $confirm, $loading) {
    var link;
    link = function($scope, $el, $attrs) {
      var form, submit, submitButton;
      form = $el.find("form").checksley({
        "onlyOneErrorElement": true
      });
      submit = debounce(2000, (function(_this) {
        return function(event) {
          var currentLoading, promise;
          event.preventDefault();
          if (!form.validate()) {
            return;
          }
          currentLoading = $loading().target(submitButton).start();
          if (!$scope.holidays.id) {
            promise = $repo.create("holidays", $scope.holidays);
            promise.then(function(data) {
              return $scope.holidays = data;
            });
          } else {
            promise = $repo.save($scope.holidays);
            promise.then(function(data) {
              return $scope.holidays = data;
            });
          }
          promise.then(function(data) {
            currentLoading.finish();
            return $confirm.notify("success");
          });
          return promise.then(null, function(data) {
            currentLoading.finish();
            form.setErrors(data);
            if (data._error_message) {
              return $confirm.notify("error", data._error_message);
            }
          });
        };
      })(this));
      submitButton = $el.find(".submit-button");
      $el.on("submit", "form", submit);
      return $el.on("click", ".submit-button", submit);
    };
    return {
      link: link
    };
  };

  module = angular.module('taigaContrib.bankholidays', []);

  module.controller("ContribBankHolidaysAdminController", BankHolidaysAdmin);

  module.directive("contribBankHolidays", ["$tgRepo", "$tgConfirm", "$tgLoading", BankHolidaysDirective]);

  initBankHolidaysPlugin = function($tgUrls) {
    return $tgUrls.update({
      "holidays": "/holidays"
    });
  };

  module.run(["$tgUrls", initBankHolidaysPlugin]);

}).call(this);
