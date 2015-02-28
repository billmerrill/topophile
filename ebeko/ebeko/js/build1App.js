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

TOPO.BUILD1.setConfig({
    'mapStartPoint': [46.852947, -121.760424],
    'elExaggerate': 1.5,
    'terrainSize': 100,
    'terrainRez': 75,
    'modelSize': 100,
    'modelRez': 200,
    'bamService': "http://127.0.0.1:8080/build",
    'pricingService': "http://127.0.0.1:8080/price",
    'uploadService': "http://127.0.0.1:8080/printer/upload",
    'modelPrintableService': "http://127.0.0.1:8080/printer/is_printable",
    'printablePause': 5000,
    'enableMsScaling': true});