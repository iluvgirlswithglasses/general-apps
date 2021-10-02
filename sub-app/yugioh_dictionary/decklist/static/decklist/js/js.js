
let effectV = $("#card-effect > p"),
    cardZoomC = $("#card-zoom"),
    cardZoomV = $("#card-zoom > img"),
    isZooming = false,
    deckV = $("#deck-view"),
    cards = {};

$(document).ready(() => {
    $.ajax({
        url: urls['get_cards'],
        data: {
            'deck_id': deckId,
        },
        dataType: 'json',
        success: (res) => {
            cards = res;
            dispDeck(cards['main']); // main deck
            dispDeck(cards['extra']); // extra deck
        }
    });
    $("#card-zoom > .close").click(() => {
        cardZoomC.hide(); isZooming = false;
        effectV.text('');
    });
});

function dispDeck(cards) {
    let containerV = $("<div class='deck container'></div>");
    deckV.append(containerV);
    for (let i in cards) {
        if (!cards.hasOwnProperty(i)) continue;
        let imgSrc = `${urls['cards_img']}/${cards[i]['id']}.jpg`;

        // card view
        let cardV = $("<img class='yugioh-card' />");
        containerV.append(cardV);
        cardV.attr('src', imgSrc);

        // card inspector view
        cardV.hover(
            () => {
                effectV.html(cards[i]['eff']);
            }, () => {
                if (!isZooming) effectV.text('');
            }
        );

        // card zoom view
        cardV.click(() => {
            cardZoomC.show(); isZooming = true;
            cardZoomV.attr('src', imgSrc);
        });
    }
}
