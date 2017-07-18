/**
 * Created by vinicius on 18/07/17.
 */

var categories = [
'	Apple pie	'
,'	Baby back ribs	'
,'	Baklava	'
,'	Beef carpaccio	'
,'	Beef tartare	'
,'	Beet salad	'
,'	Beignets	'
,'	Bibimbap	'
,'	Bread pudding	'
,'	Breakfast burrito	'
,'	Bruschetta	'
,'	Caesar salad	'
,'	Cannoli	'
,'	Caprese salad	'
,'	Carrot cake	'
,'	Ceviche	'
,'	Cheesecake	'
,'	Cheese plate	'
,'	Chicken curry	'
,'	Chicken quesadilla	'
,'	Chicken wings	'
,'	Chocolate cake	'
,'	Chocolate mousse	'
,'	Churros	'
,'	Clam chowder	'
,'	Club sandwich	'
,'	Crab cakes	'
,'	Creme brulee	'
,'	Croque madame	'
,'	Cup cakes	'
,'	Deviled eggs	'
,'	Donuts	'
,'	Dumplings	'
,'	Edamame	'
,'	Eggs benedict	'
,'	Escargots	'
,'	Falafel	'
,'	Filet mignon	'
,'	Fish and chips	'
,'	Foie gras	'
,'	French fries	'
,'	French onion soup	'
,'	French toast	'
,'	Fried calamari	'
,'	Fried rice	'
,'	Frozen yogurt	'
,'	Garlic bread	'
,'	Gnocchi	'
,'	Greek salad	'
,'	Grilled cheese sandwich	'
,'	Grilled salmon	'
,'	Guacamole	'
,'	Gyoza	'
,'	Hamburger	'
,'	Hot and sour soup	'
,'	Hot dog	'
,'	Huevos rancheros	'
,'	Hummus	'
,'	Ice_cream	'
,'	Lasagna	'
,'	Lobster bisque	'
,'	Lobster roll sandwich	'
,'	Macaroni and cheese	'
,'	Macarons	'
,'	Miso soup	'
,'	Mussels	'
,'	Nachos	'
,'	Omelette	'
,'	Onion rings	'
,'	Oysters	'
,'	Pad thai	'
,'	Paella	'
,'	Pancakes	'
,'	Panna cotta	'
,'	Peking duck	'
,'	Pho	'
,'	Pizza	'
,'	Pork chop	'
,'	Poutine	'
,'	Prime rib	'
,'	Pulled pork sandwich	'
,'	Ramen	'
,'	Ravioli	'
,'	Red velvet cake	'
,'	Risotto	'
,'	Samosa	'
,'	Sashimi	'
,'	Scallops	'
,'	Seaweed salad	'
,'	Shrimp and grits	'
,'	Spaghetti bolognese	'
,'	Spaghetti carbonara	'
,'	Spring rolls	'
,'	Steak	'
,'	Strawberry shortcake	'
,'	Sushi	'
,'	Tacos	'
,'	Takoyaki	'
,'	Tiramisu	'
,'	Tuna tartare	'
,'	Waffles	'
];

for (var i = 0; i < categories.length; i++) {
    categories[i] = categories[i].trim().toLowerCase();
}

var layer_country = null;
var layer_value = null;
var streamTime = null;

function setLayer(lys){
  layer_country = lys.getSubLayer(0);
  layer_value = lys.getSubLayer(1);

  layer_country.hide();
  layer_value.hide();
}

function refreshValueLayer(){

    layer_value.setSQL("SELECT countries_geo.*, trend_value.value FROM trend_value inner JOIN countries_geo on lower(countries_geo.name) = lower(trend_value.country)");
    layer_country.show();
    layer_value.show();

    // Run a query to get new Max / Min of layer
    // var sql = cartodb.SQL({ user: 'vinicezarml' });

    // var sublayerOptions = {
    //   sql: "SELECT * FROM trend_value WHERE 1==0"
    // };
    // layer_value.set(sublayerOptions);
}


var layerN = {};
function main() {
  map = L.map('map', {
    zoomControl: true,
    center: [10, -10],
    zoom: 3
  });

  // var hash = new L.Hash(map);

  // L.tileLayer('http://{s}.api.cartocdn.com/base-positron/{z}/{x}/{y}.png', {
  //   maxZoom: 11,
  //   attribution: 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>'
  // }).addTo(map);

  L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
    maxZoom: 9,
    attribution: 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>'
  }).addTo(map);

  var cmAttr = 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>',
               cmUrl = 'http://{s}.api.cartocdn.com/{styleId}/{z}/{x}/{y}.png';

  // var base_antique = L.tileLayer(cmUrl, {styleId: "base-antique", attribution: cmAttr});
  // var base_midnight = L.tileLayer(cmUrl, {styleId: "base-midnight", attribution: cmAttr});
  // var base_dark = L.tileLayer(cmUrl, {styleId: "base-dark", attribution: cmAttr});
  // var base_flatblue = L.tileLayer(cmUrl, {styleId: "base-flatblue", attribution: cmAttr});
  // var base_positron = L.tileLayer(cmUrl, {styleId: "base-positron", attribution: cmAttr});
  // var base_light = L.tileLayer(cmUrl, {styleId: "base-light", attribution: cmAttr});
  // var base_light_nolabels = L.tileLayer(cmUrl, {styleId: "base-light-nolabels", attribution: cmAttr});
  // var base_eco = L.tileLayer(cmUrl, {styleId: "base-eco", attribution: cmAttr});
  //
  // var baseLayers = {
  //   "Midnight": base_midnight,
  //   "Antique": base_antique,
  //   "Dark": base_dark,
  //   "FlatBlue": base_flatblue,
  //   "Light": base_light,
  //   "Light-No labels": base_light_nolabels,
  //   "Base Eco": base_eco
  // };

  // get the currently selected style
  // selectedStyle = $('li.selected').attr('id');

  cartodb.createLayer(map, 'https://hpclab.carto.com/api/v2/viz/d4e7c73f-d4d9-42ef-bad7-f18afafacd66/viz.json')
  .addTo(map)
  .done(function(lys) {
      var height_screen = $(window).height();
      $('#map').height(height_screen - 80);
      setLayer(lys);
  })
  .error(function(err) {
    console.log(err);
  });
}

function loadCategories_Selection(){
    $.each(categories, function (i, item) {
        $('#sel_category').append($('<option>', {
            value: item,
            text : item
        }));
    });
}

$(document).ready(function(){
    main();
    loadCategories_Selection();

    $('#sel_category').change(function(){
        sync_carto();
    });
});


function sync_carto() {
    // url_link = 'http://localhost:5001/cartodbview';
    url_link = 'http://test.tripbuilder.isti.cnr.it:5001/cartodbview';

    category = $('#sel_category').val();
    analysis_type = $('#sel_analysis_type').val();
    $('#img_loading').fadeIn();
    streamTime = setInterval(refreshValueLayer, 6.5 * 1000);

    $.ajax({
      type: "POST",
      url: url_link,
      async: true,
      data: { category: category, dateBegin: '20170101', dateEnd: '20170601', analysis_type: analysis_type },
      success: function (result) {
          clearInterval(streamTime);
          refreshValueLayer();
          $('#img_loading').fadeOut();

      }
    });

}

