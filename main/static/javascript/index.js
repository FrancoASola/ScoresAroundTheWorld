
// Style for Vector Layer
var styleCache = {};
var date = ''
const red = 'rgba(244, 52, 52, 0.8)'
const green = 'rgba(14, 138, 47, 0.8)'
var styleFunction = function(feature) {
  var scores = feature.get('score')
  var score = parseInt(scores.substr(0)) + parseInt(scores.substr(4))
  var radius = 5 + score;
  var style = styleCache[radius];
  if (!style) {
    style = new ol.style.Style({
      image: new ol.style.Circle({
        radius: radius,
        fill: new ol.style.Fill({
          color: red
        }),
      })
    });
    styleCache[radius] 
  }
  return style;
};

// Vector Source and Layer
var vectorSource = new ol.source.Vector({
})

var vector = new ol.layer.Vector({
  source : vectorSource,
  style: styleFunction
});

//Query goals and add to current vector layer
var params = {
  cache: false,
  type: "GET",
  success: function(data){
      // If response is valid
      var geojsonFormat = new ol.format.GeoJSON({ featureProjection: 'EPSG:3857', extractStyles: false });
      // reads and converts GeoJSon to Feature Object
      var features = geojsonFormat.readFeatures(data);
      vectorSource.clear()
      vectorSource.addFeatures(features);
      map.render()
  },
};
function getCurrentGoals(){
  if (date) {
    params.url = `api/finished/soccer/${date}`;
    params.complete = '';
  } else {
    params.url = '/api/live/soccer';
    params.complete = function() {
      // Schedule the next request when the current one's complete
      setTimeout(getCurrentGoals, 30000);
    };
  }
  $.ajax(params);
}

//Create Map
var raster = new ol.layer.Tile({
  source: new ol.source.Stamen({
    layer: 'toner'
  }),
});

var map = new ol.Map({
  layers: [raster, vector],
  target: 'map',
  view: new ol.View({
    center: [1600000, 1700000],
    zoom: 2
  })
});

getCurrentGoals()
map.render()

//Goal Information
var info = $('#info');
info.tooltip({
  animation: false,
});

var displayFeatureInfo = function(pixel) {
  info.css({
    left: pixel[0] + 'px',
    top: (pixel[1]+50) + 'px'
  });
  var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
    return feature;
  });

  if (feature) {
    info.tooltip('hide')
        .attr('data-original-title', feature.get('info'))
        // .tooltip('fixTitle')
        .tooltip('show');
  } else {
    info.tooltip('hide');
  }
};

map.on('pointermove', function(evt) {
  if (evt.dragging) {
    info.tooltip('hide');
    return;
  }
  displayFeatureInfo(map.getEventPixel(evt.originalEvent));
});

map.on('click', function(evt) {
  displayFeatureInfo(evt.pixel);
});

//Date
//Calendar
$('#picker').datetimepicker({
  timepicker: false,
  datepicker: true,
  format: 'yy-m-d', // formatDate
  closeOnDateSelect: true,
  theme: 'dark',
  yearStart:'2017',
  allowBlank: true,
  validateOnBlur: false,
  forceParse: false
});

//On Submit Date 
$('#datesubmit').on('click', function () {
  var d = $('#picker').datetimepicker('getValue');
  var year = (d.getFullYear()).toString();
  var mm = (d.getMonth() + 1).toString();
  if (mm.length < 2){
    mm = '0'+mm
  }
  var dd = (d.getDate()).toString();
  if (dd.length < 2){
    dd = '0'+dd
  }
  date = `${year}-${mm}-${dd}`
  getCurrentGoals()
});
