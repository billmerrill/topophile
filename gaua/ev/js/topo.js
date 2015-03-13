$(document).ready( function() {
    $("#how-show").easytabs(
        {
            tabs: "ul#topo-how-list > li",
            updateHash: false

        }
    ); 
    
    $("#topo-how-list li").click( function(e) {
        if (e.target.tagName != "A") {
            $("#how-show").easytabs('select', $(e.target).find("a").attr("href"));
        }
    });
});