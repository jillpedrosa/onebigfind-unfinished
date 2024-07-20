$(document).ready(function() {
    var socket = io();

    socket.on('new_lost_item', function(data) {
        var gallery = $('.found-items-gallery');
        var card = $('<div>').addClass('found-item-card');
        if (data.image) {
            card.append($('<img>').attr('src', data.image).attr('alt', data.name));
        } else {
            card.append($('<img>').attr('src', '{% static "lostandfound/images/default_item.jpg" %}').attr('alt', data.name));
        }
        card.append($('<h3>').text(data.name));
        card.append($('<p>').text('Date Found: ' + data.date_found));
        gallery.prepend(card);
    });
});