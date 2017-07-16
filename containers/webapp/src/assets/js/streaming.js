/**
 * Created by vinicius on 16/07/17.
 */

var streamTime = null

$(document).ready(function () {
    streamTime = setInterval(refreshStreaming, 90 * 1000);
});


function refreshStreaming (){
    // alert('update');
    $('#map').empty();
    $('#map').append('<iframe width="100%" height="100%" frameborder="0" src="https://hpclab.carto.com/builder/0c64c066-609e-44ce-af6b-27edd1915df6/embed" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>')

}

function stopStreaming(){
    clearInterval(streamTime);
}

