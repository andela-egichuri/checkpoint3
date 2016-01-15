// Define the application
app = angular.module('bucketlistApp', ['restangular', 'ngResource','ui.router']);

app.config(function (RestangularProvider, $interpolateProvider, $httpProvider, $resourceProvider, $urlRouterProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $resourceProvider.defaults.stripTrailingSlashes = false;
    RestangularProvider.setBaseUrl('/api');
    RestangularProvider.setRequestSuffix('/');

    // $urlRouterProvider.otherwise('/');
  });


app.controller('viewCtrl', function($scope, Restangular) {



});

app.controller('dashboardCtrl', function($scope, Restangular, $window, $controller) {
    var bucketlist = Restangular.all('bucketlists');
    bucketlist.getList().then(function(result) {
        $scope.bucketlists = result;
    });
    $scope.add = function () {
        var newbucketlist= {
          name: $scope.bl_name
        };

        bucketlist.post(newbucketlist).then(function(newbl) {
          bucketlist.getList().then(function(result) {
            $scope.bucketlists = result;
            $scope.bl_name = "";
        })
        });
    }

    $scope.edit = function (item) {
        bucketlist = Restangular.one('bucketlists', item).get()
        .then(function (result) {
            $scope.edit_name = result.name;
            $scope.bl_edit_id = item;
        })

        $('#editmodal').openModal();
    }

    $scope.delete = function (item) {
        resp = $window.confirm('Are you sure?', 'Delete');
        if (resp) {
            todelete = Restangular.one('bucketlists', item);
            todelete.remove().then(function (result) {
                bucketlist.getList().then(function(data) {
                    $scope.bucketlists = data;
                });
            });
        }
    }

    $scope.open = function (item) {
    }

    $scope.save_edit = function () {
        item = $scope.bl_edit_id;
        tosave = Restangular.one('bucketlists', item);
        tosave.name = $scope.bl_edit;
        tosave.put().then(function (result) {
            console.log(result)
            Restangular.all('bucketlists').getList().then(function(data) {
                $scope.bucketlists = data;
            });
        });
        $('#editmodal').closeModal();
    }


});
