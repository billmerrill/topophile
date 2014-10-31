var indexGeocoder = (function(){
    "use strict";
    
    var searchResultCallback,
    
    buildSearch = function(searchString) {
        /* based on example from http://open.mapquestapi.com/nominatim/ */
        var host = 'http://open.mapquestapi.com';
        var query = host + '/nominatim/v1/search.php?format=json';
        return query + "&q=" + searchString;
    },
    
    executeSearch = function(searchUrl) {
        $.ajax({
            type: "GET",
            url: searchUrl
        })
        .done(function(data, status, jqxhr) {
            searchResultCallback(data, status);
        });
    };



    return {
        init: function(searchResultCb) {
            searchResultCallback = searchResultCb;
        },
        search: function(searchString) {
            var searchUrl = buildSearch(searchString);
            executeSearch(searchUrl);
        }
    }
}());
