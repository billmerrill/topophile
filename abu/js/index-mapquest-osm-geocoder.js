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

/*
var HOST_URL = 'http://open.mapquestapi.com';
	
var EXAMPLE_BASIC = HOST_URL + '/nominatim/v1/search.php?format=json&json_callback=renderExampleBasicResults';

function showBasicURL() {
    advancedOptions = EXAMPLE_BASIC;    
	
	var query = document.getElementById("e1_query").value;
	var address = document.getElementById("e1_address_details").value;
	var limit = document.getElementById("e1_limit").value;
	var viewbox_left = document.getElementById("e1_viewbox_left").value;
	var viewbox_top = document.getElementById("e1_viewbox_top").value;
	var viewbox_right = document.getElementById("e1_viewbox_right").value;
	var viewbox_bottom = document.getElementById("e1_viewbox_bottom").value;
	var exclude = document.getElementById("e1_exclude").value;
	
	
	advancedOptions += "&q=" + query;
	if(address != ""){
		advancedOptions += "&addressdetails=" + address;
	}
	if(limit != ""){
		advancedOptions += "&limit=" + limit;
	}
	if(viewbox_left != "" && viewbox_top != "" && viewbox_right != "" && viewbox_bottom != ""){
		advancedOptions += "&viewbox=" + viewbox_left + "%2C" + viewbox_top + "%2C" + viewbox_right + "%2C" + viewbox_bottom;
	}
	if(exclude != ""){
		advancedOptions += "&exclude_place_ids=" + exclude;
	}

	
    var safe = advancedOptions;
    document.getElementById('divBasicUrl').innerHTML = safe.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/ /g, '+');
};

function doBasicClick() {
	searchType = 'basic';
    var script = document.createElement('script');
    script.type = 'text/javascript';
    showBasicURL();
    var newURL = advancedOptions;
    script.src = newURL;
    document.body.appendChild(script);
};

function renderExampleBasicResults(response) {
    var html = '';
    var i = 0;
    var j = 0;
	
	if(response){
		html += '<table><tr><th colspan="5">Search Results</th></tr>'
		html += '<tr><td><b>#</b></td><td><b>Type</b></td><td style="min-width:150px;"><b>Name</b></td><td><b>Fields</b></td><td style="min-width:200px;"><b>Address Details</b></td></tr>';
		html += '<tbody>'
		
		for(var i =0; i < response.length; i++){
			var result = response[i];
			var resultNum = i+1;
			
			html += "<tr valign=\"top\">";
			html += "<td>" + resultNum + "</td>";
			html += "<td>" + result.type + "</td>";
			
			html += "<td>";
			if(result.display_name){
				var new_display_name = result.display_name.replace(/,/g, ",<br />")
				html += new_display_name;				
			}
			html += "</td>";
			
			html += "<td>"
			if(result){
				for (var obj in result){
					var f = result[obj];
					html += "<b>" + obj + ":</b> " + f + "<br/>";					
				}
			}
			html += "</td>";
			
			html += "<td>"
			if(result.address){
				for (var obj in result.address){
					var f = result.address[obj];
					html += "<b>" + obj + ":</b> " + f + "<br/>";					
				}
			}
			html += "</td></tr>";
		}		
		html += '</tbody></table>';
	}
	
	
	switch (searchType) {
		case "basic":
			document.getElementById('divBasicResults').style.display = "";
			document.getElementById('divBasicResults').innerHTML = html;
			break;
	}
}

function collapseResults_basic(type) {
	switch(type) {
		case "basic":
			document.getElementById('divBasicResults').style.display = "none";
			break;
	}
}
*/