TOPO.BUILD1.Pricing = (function(){
    "use strict";
   
    var priceSpan, 
    
        displayPrice = function(price) {
            console.log(price)
            priceSpan.html(price);
        },
    
        getPricing = function(model_id,scale) {
            if (!scale) {
                scale = 1.0
            }
            
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('pricingService'),
                data: {'model_id': model_id,
                        'mult': scale}
            })
            .done(function(data, status, jqxhr) {
                if ('6' in data) {
                    displayPrice(data['6']);
                } else {
                    displayPrice('nope');
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
            
            updatePrice: function(model_id, scale) {
                getPricing(model_id, scale);
            }
            
        }
    
}());