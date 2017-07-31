/**
 * Created by vinicius on 18/07/17.
 */

var categories = ['apple_pie',
 'baby_back_ribs',
 'baklava',
 'beef_carpaccio',
 'beef_tartare',
 'beet_salad',
 'beignets',
 'bibimbap',
 'bread_pudding',
 'breakfast_burrito',
 'bruschetta',
 'caesar_salad',
 'cannoli',
 'caprese_salad',
 'carrot_cake',
 'ceviche',
 'cheesecake',
 'cheese_plate',
 'chicken_curry',
 'chicken_quesadilla',
 'chicken_wings',
 'chocolate_cake',
 'chocolate_mousse',
 'churros',
 'clam_chowder',
 'club_sandwich',
 'crab_cakes',
 'creme_brulee',
 'croque_madame',
 'cup_cakes',
 'deviled_eggs',
 'donuts',
 'dumplings',
 'edamame',
 'eggs_benedict',
 'escargots',
 'falafel',
 'filet_mignon',
 'fish_and_chips',
 'foie_gras',
 'french_fries',
 'french_onion_soup',
 'french_toast',
 'fried_calamari',
 'fried_rice',
 'frozen_yogurt',
 'garlic_bread',
 'gnocchi',
 'greek_salad',
 'grilled_cheese_sandwich',
 'grilled_salmon',
 'guacamole',
 'gyoza',
 'hamburger',
 'hot_and_sour_soup',
 'hot_dog',
 'huevos_rancheros',
 'hummus',
 'ice_cream',
 'lasagna',
 'lobster_bisque',
 'lobster_roll_sandwich',
 'macaroni_and_cheese',
 'macarons',
 'miso_soup',
 'mussels',
 'nachos',
 'omelette',
 'onion_rings',
 'oysters',
 'pad_thai',
 'paella',
 'pancakes',
 'panna_cotta',
 'peking_duck',
 'pho',
 'pizza',
 'pork_chop',
 'poutine',
 'prime_rib',
 'pulled_pork_sandwich',
 'ramen',
 'ravioli',
 'red_velvet_cake',
 'risotto',
 'samosa',
 'sashimi',
 'scallops',
 'seaweed_salad',
 'shrimp_and_grits',
 'spaghetti_bolognese',
 'spaghetti_carbonara',
 'spring_rolls',
 'steak',
 'strawberry_shortcake',
 'sushi',
 'tacos',
 'takoyaki',
 'tiramisu',
 'tuna_tartare',
 'waffles'];

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

var session = uuidv4();
var custom = false;

// for (var i = 0; i < categories.length; i++) {
//     categories[i] = categories[i].trim().toLowerCase();
// }

var layer_country = null;
var layer_value = null;
var streamTime = null;

function setLayer(lys){
      // layer_country = lys[1].getSubLayer(0);
      layer_value = lys[1].getSubLayer(0);

      // layer_country.show();
      layer_value.hide();

}

function refreshValueLayer(){

    if (custom){
        layer_value.setSQL("SELECT countries_geo.*, trend_value.value, trend_value.country, trend_value.category, trend_value.analysis_type	FROM trend_value inner JOIN countries_geo on lower(countries_geo.name) = lower(trend_value.country) WHERE trend_value.session = '" + session + "'");
        // layer_country.show();
        // layer_value.show();
    }
    else {
        // alert('refresh layer');
        var category = $('#sel_category').val();
        var analysis_type = $('#sel_analysis_type').val();
        var interval = $('#sel_interval').val();

        layer_value.setSQL("SELECT countries_geo.*, trend_value.value, trend_value.country, trend_value.category, trend_value.analysis_type	FROM trend_value inner JOIN countries_geo on lower(countries_geo.name) = lower(trend_value.country) " +
            "WHERE trend_value.category = '" + category + "' and analysis_type = '" + analysis_type + "' and interval = " + interval + "" );
        // layer_country.show();
        layer_value.show();
    }

    alert("SELECT countries_geo.*, trend_value.value, trend_value.country, trend_value.category, trend_value.analysis_type	FROM trend_value inner JOIN countries_geo on lower(countries_geo.name) = lower(trend_value.country) " +
            "WHERE trend_value.category = '" + category + "' and analysis_type = '" + analysis_type + "' and interval = " + interval + "")

    // Run a query to get new Max / Min of layer
    // var sql = cartodb.SQL({ user: 'vinicezarml' });

    // var sublayerOptions = {
    //   sql: "SELECT * FROM trend_value WHERE 1==0"
    // };
    // layer_value.set(sublayerOptions);
}

function ucFirstAllWords( str )
{
    var pieces = str.split(" ");
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1);
    }
    return pieces.join(" ");
}


function loadCategories_Selection(){
    $.each(categories, function (i, item) {
        $('#sel_category').append($('<option>', {
            value: item,
            text : ucFirstAllWords(item.replace(/_/g,' '))
        }));
    });
}


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
      data: { category: category, dateBegin: '20170101', dateEnd: '20170601', analysis_type: analysis_type, session: session },
      success: function (result) {
          clearInterval(streamTime);
          refreshValueLayer();
          $('#img_loading').fadeOut();

      }
    });

}

var layerN = {};
function main() {
  // map = L.map('map', {
  //   zoomControl: true,
  //   center: [10, -10],
  //   zoom: 3
  // });

  // var hash = new L.Hash(map);

  // L.tileLayer('http://{s}.api.cartocdn.com/base-positron/{z}/{x}/{y}.png', {
  //   maxZoom: 11,
  //   attribution: 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>'
  // }).addTo(map);

  // L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
  //   maxZoom: 9,
  //   attribution: 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>'
  // }).addTo(map);
  //
  // var cmAttr = 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>',
  //              cmUrl = 'http://{s}.api.cartocdn.com/{styleId}/{z}/{x}/{y}.png';

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

  // cartodb.createLayer(map, 'https://hpclab.carto.com/api/v2/viz/d4e7c73f-d4d9-42ef-bad7-f18afafacd66/viz.json')
  // .addTo(map)
  // .done(function(lys) {
  //     var height_screen = $(window).height();
  //     $('#map').height(height_screen - 80);
  //     setLayer(lys);
  // })
  // .error(function(err) {
  //   console.log(err);
  // });

    var options = {
        shareable: false,
        title: true,
        description: false,
        search: true,
        tiles_loader: false,
        center_lat: 10,
        center_lon: 8.5,
        zoom: 3,
        cartodb_logo: true
    };
    var vizjson = 'https://hpclab.carto.com/api/v2/viz/d4e7c73f-d4d9-42ef-bad7-f18afafacd66/viz.json'
    // var vizjson = 'https://vinicezarml.carto.com/api/v2/viz/de0aa1d3-4fcd-44e9-b824-b89e7cb48744/viz.json'
    var height_screen = $(window).height();
    $('#map').height(height_screen - 120);

    cartodb.createVis('map',vizjson,options).done(function(vis, layers) {
        // $('#map').height(height_screen - 80);
        setLayer(layers);
    });

}

function set_interval(){
    var selected_analysis_type =$('#sel_analysis_type').val();
    if(selected_analysis_type == 'popularity' || selected_analysis_type == 'trend'){
        $('#sel_interval').removeAttr("disabled");
    }
    else {
        $('#sel_interval').attr("disabled", "disabled");
    }
}


$(document).ready(function(){
    main();
    loadCategories_Selection();
    set_interval();


    $('#sel_interval').change(function(){
        if (custom){
            sync_carto();
        }
        else {
            refreshValueLayer();
        }
    });


    $('#sel_category').change(function(){
        if (custom){
            sync_carto();
        }
        else {
            refreshValueLayer();
        }
    });

    $('#sel_analysis_type').change(function(){
        set_interval();
        if ($('#sel_category').val() != 0){
            if (custom){
                sync_carto();
            }
            else {
                refreshValueLayer()
            }
        }
    });


});
