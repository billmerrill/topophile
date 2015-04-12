TOPO.BUILD1.Pricing = (function(){
    "use strict";
   
    var priceSpan, 
    
        displayPrice = function(price) {
            price = price.toFixed(0);
            priceSpan.html('$' + price);
        },
        
        displayMsg = function(msg) {
            priceSpan.html(msg);    
        },
    
        getPricing = function(model_id) {
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('pricingService'),
                data: {'model_id': model_id}
            })
            .done(function(data, status, jqxhr) {
                if ('6' in data) {
                    displayPrice(data['6']);
                } else {
                    displayMsg('nope');
                }
            })
            .fail(function(data) {
                displayPrice('error');
            });
        };
        
        return {
            init: function(priceSpanId) {
                priceSpan = $('#'+priceSpanId);
            },
            
            clearPrice: function() {
                displayMsg("...");
            },
            
            updatePrice: function(model_id) {
                displayMsg("...");
                getPricing(model_id);
            },
            
            
        }
    
}());