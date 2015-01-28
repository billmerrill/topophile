var TOPO = TOPO || {};
TOPO['BUILD1']= {};


TOPO.BUILD1.setConfig = function(conf) {
    TOPO.BUILD1.config = conf;
}

TOPO.BUILD1.getConfig = function(key) {
    if (key) {
        return TOPO.BUILD1.config[key];
    } else {
        return TOPO.BUILD1.config;
    }
}