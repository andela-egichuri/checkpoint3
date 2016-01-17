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
    // $resourceProvider.defaults.stripTrailingSlashes = false;
    RestangularProvider.setBaseUrl('/api');
    RestangularProvider.setRequestSuffix('/');
    // $routeProvider.
    //         when('/', {
    //             templateUrl : 'static/views/bucketlists.html',
    //             controller  : 'dashboardCtrl'
    //         }).
    //         when('/bucketlist/:bid', {
    //             templateUrl : 'static/views/bucketlist.html',
    //             controller  : 'BucketlistCtrl'
    //         })

    // $urlRouterProvider.otherwise('/bucketlists');
    // $stateProvider
    //   .state('bucketlists', {
    //     url: '/bucketlists',
    //     templateUrl: 'static/views/bucketlists.html',
    //     controller: 'dashboardCtrl',
    //   })
    //   .state('bucketlist', {
    //     url: 'bucketlists/:id',
    //     templateUrl: 'static/views/bucketlists.html',
    //     controller: 'BucketlistCtrl',
    //   })

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
    bucketlist.getList().then(function(result) {
        $scope.bucketlists = result;
    });
    $scope.add = function () {
        var newbucketlist= {
          name: $scope.bl_name,
        };

        bucketlist.post(newbucketlist).then(function(newbl) {
          bucketlist.getList().then(function(result) {
            $scope.bucketlists = result;
            $scope.bl_name = "";
            angular.element('.collapsible-header').trigger('click');

        })
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
                Restangular.all('bucketlists').getList().then(function(data) {
                    $scope.bucketlists = data;
                });
            });
        }
    }

    $scope.save_edit = function () {
        value = $scope.bl_edit_id;
        tosave = Restangular.one('bucketlists', value);
        tosave.name = $scope.bl_edit;
        tosave.put().then(function (result) {
            Restangular.all('bucketlists').getList().then(function(data) {
                $scope.bucketlists = data;
            });
        });
        $scope.bl_edit = "";
        $('#editmodal').closeModal();
    }


});
