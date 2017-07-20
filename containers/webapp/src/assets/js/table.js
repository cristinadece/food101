/**
 * Created by vinicius on 17/07/17.
 */

var countries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas'
    , 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire, saint eustatius and saba ', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory'
    , 'british virgin islands', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos islands', 'colombia', 'comoros'
    , 'cook islands', 'costa rica', 'croatia', 'cuba', 'curacao', 'cyprus', 'czech republic', 'democratic republic of the congo', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea'
    , 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada'
    , 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle of man', 'israel'
    , 'italy', 'ivory coast', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia'
    , 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique'
    , 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands antilles', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'north korea', 'northern mariana islands', 'norway', 'oman', 'pakistan'
    , 'palau', 'palestinian territory', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'republic of the congo', 'reunion', 'romania', 'russia', 'rwanda', 'saint barthelemy'
    , 'saint helena', 'saint kitts and nevis', 'saint lucia', 'saint martin', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'serbia and montenegro'
    , 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'south korea', 'south sudan', 'spain', 'sri lanka', 'sudan'
    , 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan'
    , 'turks and caicos islands', 'tuvalu', 'u.s. virgin islands', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu'
    , 'vatican', 'venezuela', 'vietnam', 'wallis and futuna', 'western sahara', 'yemen', 'zambia', 'zimbabwe']

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

// for (var i = 0; i < categories.length; i++) {
//     categories[i] = categories[i].trim().toLowerCase();
//}

function loadCountries_Selection(){
    $.each(countries, function (i, item) {
        $('#sel_country').append($('<option>', {
            value: item,
            text : item
        }));
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


function set_viewmode(sel_value){

    if (sel_value == 'bycategory'){
        $('#div_bycountry').hide();
        $('#div_chart').hide();
        $('#div_bycategory').show();
    }
    else if (sel_value == 'bycountry') {
        $('#div_bycountry').show();
        $('#div_chart').hide();
        $('#div_bycategory').hide();
    }
    else {
        $('#div_bycountry').hide();
        $('#div_chart').show();
        $('#div_bycategory').hide();
    }
}

$(document).ready(function(){

    set_viewmode($('#sel_view_mode').val());
    loadCategories_Selection();
    loadCountries_Selection();

    $('#sel_category').change(function(){
        get_bycategory();
    });

    $('#sel_country').change(function(){
        get_bycountry();
    });

    $('#sel_view_mode').change(function(e){
        sel_value = $(this).val();
        set_viewmode(sel_value);
    });

    $('#sel_analysis_type').change(function(e) {

        if($('#sel_category').val() != 0){
            get_bycategory();
        }

        if($('#sel_country').val() != 0){
            get_bycountry();
        }
    });

});

function get_bycategory(){
    // url_link = 'http://localhost:5001/countriestrends'
    url_link = 'http://test.tripbuilder.isti.cnr.it:5001/countriestrends'


    category = $('#sel_category').val();
    analysis_type = $('#sel_analysis_type').val();
    $('#lbl_value_bycategory').html(analysis_type);

    $.ajax({
      type: "POST",
      url: url_link,
      data: { category: category, dateBegin: '20170101', dateEnd: '20170601', analysis_type: analysis_type },
      success: function (result) {
          result = JSON.parse(result);
          results = result['results'];
          idx = 1;
          $("#tb_bycategory > tbody").empty();

          for (idx_country in results){

              country = results[idx_country];
              var value_exhibition = country['value']
              if (analysis_type == 'frequency'){
                  value_exhibition= parseInt(value_exhibition)
              } else {
                  value_exhibition = parseFloat(value_exhibition).toFixed(4)
              }

              $('#tb_bycategory > tbody:last-child').append('<tr>' +
              '<td>' + idx + ' </td>' +
              '<td>' + country['country'] + '</td>' +
              '<td>' + value_exhibition + '</td>' +
              '</tr>');
              idx = idx + 1

              if (idx > 20){
                  break
              }
          }
      }
    });
}


function get_bycountry(){
    // url_link = 'http://localhost:5001/categoriestrends'
    url_link = 'http://test.tripbuilder.isti.cnr.it:5001/categoriestrends'

    country = $('#sel_country').val();
    analysis_type = $('#sel_analysis_type').val();

    $.ajax({
      type: "POST",
      url: url_link,
      data: { country: country, dateBegin: '20170101', dateEnd: '20170601', analysis_type: analysis_type },
      success: function (result) {
          result = JSON.parse(result);
          results = result['results'];
          idx = 1;
          $("#tb_bycountry > tbody").empty();
          $('#lbl_value_bycountry').html(analysis_type);

          for (idx_category in results){
              var category = results[idx_category];
              var value_exhibition = category['value']
              if (analysis_type == 'frequency'){
                  value_exhibition= parseInt(value_exhibition)
              } else {
                  value_exhibition = parseFloat(value_exhibition).toFixed(4)
              }

              $('#tb_bycountry > tbody:last-child').append('<tr>' +
              '<td>' + idx + ' </td>' +
              '<td>' + category['category'] + '</td>' +
              '<td>' + value_exhibition + '</td>' +
              '</tr>');
              idx = idx + 1

              if (idx > 20){
                  break
              }
          }
      }
    });
}