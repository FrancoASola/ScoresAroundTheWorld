
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
})

var vector = new ol.layer.Vector({
  source : vectorSource,
  style: styleFunction
});

function getCurrentGoals(){
  $.ajax({
    cache: false,
    type: "GET",
    url: "/static/soccer.geojson",
    success:function(data){
        // If response is valid
        var geojsonFormat = new ol.format.GeoJSON({ featureProjection: 'EPSG:3857' });
        // reads and converts GeoJSon to Feature Object
        var features = geojsonFormat.readFeatures(data);
        vectorSource.clear()
        console.log(vectorSource.features)
        vectorSource.addFeatures(features);
        console.log(features),
        map.render()
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(getCurrentGoals, 5000);
    }
  });
}

var raster = new ol.layer.Tile({
  source: new ol.source.OSM({
  })
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

