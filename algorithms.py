from Cards import value, all_cards

player_cards = {
    "H": [],
    "D": [],
    "C": [],
    "S": [],
}

remaining_cards = {
    "S": [
        '1S', 'KS', 'QS', 'JS', 'TS', '9S', '8S', '7S', '6S', '5S', '4S', '3S',
        '2S'
    ],
    "H": [
        '1H', 'KH', 'QH', 'JH', 'TH', '9H', '8H', '7H', '6H', '5H', '4H', '3H',
        '2H'
    ],
    "D": [
        '1D', 'KD', 'QD', 'JD', 'TD', '9D', '8D', '7D', '6D', '5D', '4D', '3D',
        '2D'
    ],
    "C": [
        '1C', 'KC', 'QC', 'JC', 'TC', '9C', '8C', '7C', '6C', '5C', '4C', '3C',
        '2C'
    ],
}

neg_factor = 0.75


def card_manager(cards):
    """
    This function sorts users card in a proper dictionary to make card chosing
    easier and faster when playing.
    """

    global player_cards

    for _ in player_cards.values(
    ):  # to clear the cards stored from previous round
        _.clear()

    for card in cards:
        # adds the card to its respective set
        player_cards[card[1]].append(card)

    for _ in player_cards.values():
        _.sort(key=lambda x: value[x])  # sorts the set of cards

    return player_cards


def bid_calculator(cards):
    """
    This function calculates weight of all the cards and use a mathemtical formula
    to calculate the bid value:

    The least possible weight to achieve is 35 i.e 2H, 2C, 2D, 3H, 3C, 3D, 
    4H, 4C, 4D, 5H, 5C, 5D, 6 of any besides spade. So in this case the bid value
    will be 0.
    Similarly the maximum possible weight to achieve is 260 i.e having all spades.
    So in this case the bid value will be 13.

    So this functino compresses the weight range i.e. 35-260 to bid range 
    i.e 0-13

    This functin also checks the shape density, greater the no of same kind 
    of cards lower the bid

    Formula:
    weightRange = maxWeight - minWeight
    bidRange = maxBid - minBid
    bidValue = (((weight - minWeight) * bidRange) / weightRange) + minBid

    """

    weight = -35
    local_neg_factor = neg_factor
    spades, hearts, diamonds, clubs = card_manager(
        cards)  # this return list of sorted cards

    for card in cards:
        weight += value[card]

    bid = (4 * weight) / 113

    if bid >= 5:
        local_neg_factor *= 2

    #  thus if else block reduces the bid by a factor if there are more that 3 crads of same kind
    if clubs.__len__() > 3:
        bid -= local_neg_factor * clubs.__len__() / 4
    if hearts.__len__() > 3:
        bid -= local_neg_factor * hearts.__len__() / 4
    if diamonds.__len__() > 3:
        bid -= local_neg_factor * diamonds.__len__() / 4

    if int(bid) <= 0:  # incase the bid goes negetive
        bid = 1

    return int(bid)


def remove_cards(cards):
    for card in cards:
        remaining_cards[card[1]].remove(card[:2])
        remaining_cards[card[1]].append(card[:2])


def play_card_index(info: dict):
    cards = info["cards"]
    card_manager(cards)

    played = info["played"]
    larger = False

    least_diff = 30
    to_play = cards[0]
    ind = 0

    if info['history']:
        remove_cards(info["history"][-1][1])

    if played:
        # determine the top card on the ground
        top, shape = played[0][:2], played[0][1]
        for card in played:
            card = card[:2]
            if card[1] in {shape, "S"}:
                if value[card] > value[top]:
                    top = card
        # this block changes the shape of the card to be played if the player doesn't have required shaped card
        if not player_cards[shape]:
            if player_cards["S"]:
                shape = 'S'
            else:
                # this determines the which shape card does the user have the most if they lack spades too
                length = 0
                for shapes in player_cards:
                    if player_cards[shapes].__len__() > length:
                        shape = shapes
                        length = player_cards[shapes].__len__()
            top = '2H'  # since the user is going to loose anyways as it doesn't have required shaped cards so least possible card is chosen.

        # this block determines the card to be thrown(either just higher or least valued card)
        for card in player_cards[shape]:
            if info['history'].__len__() > 2 and remaining_cards[shape][0] in player_cards[shape] and played.__len__() < 3:
                # this block plays the top most card from round 2 of same color to secure the win
                to_play = remaining_cards[shape][0]
            else:
                # this block plays normally before round 2 or the user doesnt have the highest card of the reqd color
                diff = value[card] - value[top]
                if diff >= 0:
                    # this block determines the card that is just higher than that on the ground.
                    if least_diff <= 0:
                        least_diff = 30
                    if diff < least_diff:
                        least_diff = diff
                        to_play = card
                        larger = True
                else:
                    # this block determines the least valued card if the user doesnt have the higher card
                    if diff < least_diff and not larger:
                        least_diff = diff
                        to_play = card
    else:
        # this block determines the card to be thrown when the user is the first player
        found_card = False
        for shape in player_cards:
            # this block searches for the top most card of the shape, jun chai hami sanga 3 ta bhanda dherai xa
            if player_cards[shape].__len__() > 2 and shape != "S" and remaining_cards[shape][0] in player_cards[shape]:
                to_play = remaining_cards[shape][0]
                found_card = True
        if not found_card:
            # this block searches for the least valued card of the shape which we have the most/least (Note: use key_len=13 or least and 0 or most)
            to_play_shape = list(player_cards.keys())[0]
            # key_len = 0
            key_len = 13
            for shape in player_cards:
                if 0 < player_cards[shape].__len__() < key_len:
                    key_len = player_cards[shape].__len__()
                    to_play_shape = shape
                    to_play = player_cards[to_play_shape][0]
            
        ind = cards.index(to_play)
    

    return ind


# test = [
#     ['JC', '7D', '9H', 'QD', '6C', 'JH', '2S', 'QS', 'JD', '3S', 'KH', '2D', '6S'],
#     ['2H', '5C', 'JH', '6C', 'QH', 'TD', 'QS', '8C', '1S', '5D', '9C', '7H', '6S'],
#     ['9C', '6H', '7D', 'JS', '9S', '4D', '6C', 'JC', 'KH', '2S', 'KD', '4D', '3C'],
#     ['3S', '3D', '5S', '4H', '2D', '2D', '4D', '9S', '4C', '9H', '1H', 'QD', '2D'],
#     ['5D', '1C', '1H', 'KS', 'QC', 'TS', '6H', '4S', 'QD', '1S', 'JH', '8D', '3H'],
#     ['8S', '7D', '7D', '3C', 'TH', 'JS', 'QS', '9D', '5H', 'JH', 'QS', 'QC', '5D'],
#     ['TC', 'TS', '3S', '7D', 'JH', '1H', '9C', 'QC', 'JD', '5S', '7S', 'TS', '1C'],
#     ['2C', '1S', '8H', '7D', 'QD', '6C', '2H', 'QS', '4H', 'KC', '3S', 'TC', 'KC'],
#     ['KH', '6D', '3C', 'QC', 'KC', '4D', '6C', '5H', '8C', '2H', '6D', '6H', 'QC'],
#     ['QD', 'TC', '7S', '7S', '8D', '7D', '3D', '5S', '3H', '3S', '6C', 'KS', '9D']
# ]

# for i in test:
#     print(i)
#     print(bid_calculator(i))

info = {
    "cards": [
        "1S", "TS", "7S", "6S", "1H", "KH", "QH", "JH", "4H", "1C", "QC", "TC", "8D"
    ],
    "played": [
        "7D/0", "JD/0", "KC/0" 
    ],
    "history": [
        [1, ["5S/0", "9S/0", "TS/0", "QS/0"], 4],
        [1, ["6D/0", "1D/0", "4D/0", "8D/0"], 4],
        [1, ["5C/0", "2C/0", "TC/0", "JC/0"], 4]
    ]
}

# print(play_card_index(info))
# print(bid_calculator(["1S","TS", "7S", "6S", "1H", "KH", "QH", "JH", "4H", "1C", "QC", "TC", "8D"]))
# remove_cards(test[0])
# print(remaining_cards)