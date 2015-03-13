$(document).ready( function() {
    $("#topo-walkthru").easytabs(
        {
            tabs: "ul#topo-walkthru-list > li",
            updateHash: false

        }
    ); 
    
    $("#topo-walkthru-list li").click( function(e) {
        if (e.target.tagName != "A") {
            $("#topo-walkthru").easytabs('select', $(e.target).find("a").attr("href"));
        }
    });
});