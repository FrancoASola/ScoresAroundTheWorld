
var styleCache = {};
var styleFunction = function(feature) {
  var name = feature.get('name');
  //var score = parseFloat(name.substr(2));
  var radius = 5;
  var style = styleCache[radius];
  if (!style) {
    style = new ol.style.Style({
      image: new ol.style.Circle({
        radius: radius,
        fill: new ol.style.Fill({
          color: 'rgba(240, 52, 52, 0.4)'
        }),
        stroke: new ol.style.Stroke({
          color: 'rgba(255, 204, 0, 0.2)',
          width: 5
        })
      })
    });
    styleCache[radius] = style;
  }
  return style;
};

var vectorSource = new ol.source.Vector({
  format: new ol.format.GeoJSON()
})

var vector = new ol.layer.Vector({
  title: 'b_layer',
  source : vectorSource,
  style: styleFunction
});

$.ajax({
  type: "GET",
  url: "/static/soccer.geojson",
  dataType:"json",
  success:function(data){
      // If response is valid
      var geojsonFormat = new ol.format.GeoJSON();

      // reads and converts GeoJSon to Feature Object
      var features = geojsonFormat.readFeatures(data);
      vectorSource.addFeatures(features);
  }
});

var raster = new ol.layer.Tile({
  source: new ol.source.OSM({
  })
});

var map = new ol.Map({
  layers: [raster],
  target: 'map',
  view: new ol.View({
    center: [1600000, 1700000],
    zoom: 2
  })
});

map.addLayer(vector)
map.render()
// // var info = $('#info');
// // info.tooltip({
// //   animation: false,
// //   trigger: 'manual'
// // });

// var displayFeatureInfo = function(pixel) {
//   info.css({
//     left: pixel[0] + 'px',
//     top: (pixel[1] - 15) + 'px'
//   });
//   var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
//     return feature;
//   });
//   if (feature) {
//     info.tooltip('hide')
//       .attr('data-original-title', feature.get('name'))
//       .tooltip('fixTitle')
//       .tooltip('show');
//   } else {
//     info.tooltip('hide');
//   }
// };

// map.on('pointermove', function(evt) {
//   if (evt.dragging) {
//     info.tooltip('hide');
//     return;
//   }
//   displayFeatureInfo(map.getEventPixel(evt.originalEvent));
// });

// map.on('click', function(evt) {
//   displayFeatureInfo(evt.pixel);
// });

