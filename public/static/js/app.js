// Define the application
app = angular.module('bucketlistApp', ['restangular', 'ngResource', 'ui.router']);

app.config(function (RestangularProvider, $interpolateProvider, $httpProvider, $stateProvider, $locationProvider, $urlRouterProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
     $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
    RestangularProvider.setBaseUrl('/api');
    RestangularProvider.setRequestSuffix('/');
    RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
      var extractedData;
      // .. to look for getList operations
      if (operation === "getList") {
        // .. and handle the data and meta data
        extractedData = data.results;
        extractedData.next = data.next;
        extractedData.previous = data.previous;
        extractedData.count = data.count;
      } else {
        extractedData = data;
      }
      return extractedData;
    });

  });


app.controller('bucketlistCtrl', function($scope, Restangular, $window) {
    bid = $scope.bid
    bucketlist = Restangular.one('bucketlists', bid);
    bucketlist.get().then(function (result) {
        $scope.bucketlist_name = result.name;
    })
    bucketlist.getList('items').then(function(result) {
        $scope.bucketlist = result;
    });

    $scope.add = function () {
        var newitem= {
          name: $scope.it_name,
          bucketlist: $scope.bid
        };
        bucketlist.post('items', newitem).then(function(item) {
          bucketlist.getList('items').then(function(result) {
            $scope.bucketlist = result;
            $scope.it_name = "";

        })
        });

    }

    $scope.delete = function(item) {
        resp = $window.confirm('Delete item? This action is not reversible');
        if (resp) {
            todelete = Restangular.one('bucketlists', $scope.bid).one('items', item);
            todelete.remove().then(function (result) {
                bucketlist.getList('items').then(function(result) {
                    $scope.bucketlist = result;
                });
            });
        };
    };

    $scope.edititem = function (value) {
        item = Restangular.one('bucketlists', $scope.bid).one('items', value).get()
        .then(function (result) {
            $scope.item_edit = result.name;
            $scope.item_edit_id = value;

            $scope.donestatus = result.done;;
        })

        $('#itemmodal').openModal();
    }

    $scope.status = function(item, current) {
        toedit = Restangular.one('bucketlists', $scope.bid).one('items', item);
        if (current) {
            toedit.done = 0;
        }
        else {
            toedit.done = 1;
        }
        toedit.bucketlist = $scope.bid;
        toedit.get().then(function (result) {
            toedit.name = result.name;
            toedit.put().then(function (result) {
            bucketlist.getList('items').then(function(result) {
                $scope.bucketlist = result;
            });
        });

        })

    };

    $scope.saveitem = function () {
        value = $scope.item_edit_id;
        tosave = Restangular.one('bucketlists', $scope.bid).one('items', value);
        tosave.name = $scope.item_edit;
        tosave.bucketlist = $scope.bid;
        tosave.done = $scope.donestatus;
        tosave.put().then(function (result) {
            bucketlist.getList('items').then(function(result) {
                $scope.bucketlist = result;
            });
        });
        $scope.item_edit = "";
        $('#itemmodal').closeModal();
    }

});


app.controller('dashboardCtrl', function($scope, Restangular, $window) {
    var bucketlist = Restangular.all('bucketlists');
    $scope.page = 1
    $scope.count = [];
    bucketlist.getList({page: $scope.page}).then(function(result) {
        $scope.pages = Math.ceil(result.count / 6);
        $scope.count = new Array($scope.pages);
        $scope.bucketlists = result;
        $scope.next = result.next;
        $scope.previous = result.previous
    });

    $scope.refresh = function () {
        bucketlist.getList({page: $scope.page}).then(function(result) {
            $scope.pages = Math.ceil(result.count / 6);
            $scope.count = new Array($scope.pages);
            $scope.bucketlists = result;
            $scope.next = result.next;
            $scope.previous = result.previous
        });
    }

    $scope.setpage = function (value) {
        if (value > 0 && value <= $scope.pages) {
            $scope.page = value
        }
        $scope.refresh();
    }

    $scope.add = function () {
        var newbucketlist= {
          name: $scope.bl_name,
        };

        bucketlist.post(newbucketlist).then(function(newbl) {
            $scope.refresh();
            $scope.bl_name = "";
            angular.element('.collapsible-header').trigger('click');
        });

    }

    $scope.edit = function (value) {
        bucketlist = Restangular.one('bucketlists', value).get()
        .then(function (result) {
            $scope.bl_edit = result.name;
            $scope.bl_edit_id = value;
        })

        $('#editmodal').openModal();
    }

    $scope.delete = function (value) {
        resp = $window.confirm('Delete bucketlist? Its items will also be deleted');
        if (resp) {
            todelete = Restangular.one('bucketlists', value);
            todelete.remove().then(function (result) {
                $scope.refresh();
            });
        }
    }

    $scope.save_edit = function () {
        value = $scope.bl_edit_id;
        tosave = Restangular.one('bucketlists', value);
        bucketlist = Restangular.all('bucketlists');
        tosave.name = $scope.bl_edit;
        tosave.put().then(function (result) {
            $scope.refresh();
        });
        $scope.bl_edit = "";
        $('#editmodal').closeModal();
    }


});
