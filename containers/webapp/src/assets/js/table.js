/**
 * Created by vinicius on 17/07/17.
 */

countries = ['brazil', 'italy', 'japan'];

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
              $('#tb_bycategory > tbody:last-child').append('<tr>' +
              '<td>' + idx + ' </td>' +
              '<td>' + country['country'] + '</td>' +
              '<td>' + parseFloat(country['value']).toFixed(2) + '</td>' +
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
              category = results[idx_category];
              $('#tb_bycountry > tbody:last-child').append('<tr>' +
              '<td>' + idx + ' </td>' +
              '<td>' + category['category'] + '</td>' +
              '<td>' + parseFloat(category['value']).toFixed(4) + '</td>' +
              '</tr>');
              idx = idx + 1

              if (idx > 20){
                  break
              }
          }
      }
    });
}