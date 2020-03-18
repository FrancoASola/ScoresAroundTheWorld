
// Style for Vector Layer
var styleCache = {};
var date = ''
const red = 'rgba(244, 52, 52, 0.8)'
const green = 'rgba(14, 138, 47, 0.8)'
var styleFunction = function(feature) {
  var scores = feature.get('score')
  var score = parseInt(scores.substr(0)) + parseInt(scores.substr(4))
  var radius = 10 + score;
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
var customRes = [156543.0339, 78271.51695, 39135.758475, 19567.8792375, 9783.93961875, 4891.969809375, 2445.9849046875, 1222.99245234375, 611.496226171875, 305.7481130859375, 152.87405654296876, 76.43702827148438, 38.21851413574219, 19.109257067871095, 9.554628533935547, 4.777314266967774, 2.388657133483887, 1.1943285667419434, 0.5971642833709717,0.41999977320012255, 0.2799998488000817,0.13999992440004086, 0.08399995464002451, 0.05599996976001634, 0.02799998488000817] 
var raster = new ol.layer.Tile({
  source: new ol.source.Stamen({
    layer: 'toner'
  }),
});

var map = new ol.Map({
  interactions : ol.interaction.defaults({doubleClickZoom :false}),
  layers: [raster, vector],
  target: 'map',
  view: new ol.View({
    resulotions: customRes,
    center: [1600000, 1700000],
    resolution: 50000
  })
});

getCurrentGoals()
map.render()

//Match Tooltip
var info = $('#info');
info.tooltip({
  animation: false,
});

var displayFeatureInfo = function(pixel) {
  var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
    return feature;
  });
  if (feature) {
    info.css({
      left: pixel[0] + 'px',
      top: (pixel[1] + $('#navbar').height()) + 'px',
    });
    info.tooltip('hide')
        .attr('data-original-title', feature.get('info'))
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

//Match Comment Box 

//Connect Socket (This can be used to POST live games to Client from Server)
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', function() {
});
var displayChatBox = function(pixel){
  //Check if feature exists where client is double clicking
  var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
    return feature;
  });
  //If there is feature open chatbox (setting name and styles), load messages and join chat room.
  if (feature) {
    var match_id = feature.get('match_id')
    $('p[id^="match"]').html(feature.get('info'))
    $('p[id^="match"]').attr('name', match_id)
    $('#msg_history').empty()
    loadMessages(match_id)
    socket.emit('join', {'match_id': match_id})
    $('#chatbox').css({
      top: $('#navbar').height(),
    }),
    document.getElementById("chatbox").style.display = "block";
  }
}

//Open Match Message Board
map.on('dblclick', function(evt){
  info.tooltip('hide');
  displayChatBox(map.getEventPixel(evt.originalEvent));
});

//Send Messages
$('#send').on('click', function(){
  match_id = $('p[id^="match"]').attr('name')
  sendMessage()
  $("#messagebox").val('')
});

$('#messagebox').keydown(function(e){
  if(e.which==13){
    match_id = $('p[id^="match"]').attr('name')
    sendMessage()
    $("#messagebox").val('')
  }
});
function sendMessage(){
  socket.emit('post_message', {'text': $('#messagebox').val()})
}

//Receive Messages
socket.on('load_message', data => {
  $.each(data, add_message)
})

//Load Messages (pulling from DB)
function loadMessages(match_id){
  $.ajax({
    type: 'GET',
    url: `api/messages/${match_id}`,
    success: function(data){
      $.each(data['messages'], add_message);
    }
  })
}

//Close Match Message Board
$('#closeChat').on('click', function () {
  document.getElementById("chatbox").style.display = "none";
  socket.emit('leave', {})
});

//Add messages to chat
function add_message(key, value){
  $('<div>',{
    class: "received_msg"
  }).append( $('<div>',{
    class: "received_withd_msg"
  }).append( $('<p>'
  ).append(
    value[0]['text']))
  ).append( $('<span>',{
    class: "time_date"
  }).append(`${value[0]['time']} | ${value[0]['date']}`)
  ).appendTo('#msg_history')
  $('#msg_history').scrollTop($('#msg_history')[0].scrollHeight);
}

//Back and forth between messages and highlights

$('#msg_hl_switcher').on('click', function () {
  if ($("#msg_hl_switcher").html() === 'Highlights'){
    document.getElementById("msg_history").style.display = "none";
    document.getElementById("hl_history").style.display = "block";
    $("#msg_hl_switcher").html('Messages');
  } else {
    document.getElementById("msg_history").style.display = "block";
    document.getElementById("hl_history").style.display = "none";
    $("#msg_hl_switcher").html('Highlights');
  }
});


//Find Finished Games
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

//On Submit Date (Need to speed up this process on server side)
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
  vectorSource.clear()
  window.history.pushState({'title' : date}, 'Finished Games', date);
  getCurrentGoals()
});


