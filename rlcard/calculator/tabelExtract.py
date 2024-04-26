import rlcard.utils.utils
import parallel_holdem_calc as calc
import json
from rlcard.games.base import Card


def calculate_semiknown_oddstable(indices):
    # calculate the odds with only your hand known
    odds_table = {}
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            odds = calc.calculate(None, True, 1, None, [indices[i], indices[j], '?', '?'], False)
            odds_table[(indices[i], indices[j])] = odds

def calculate_semiknown_basedonSuit(indices):
    odds_table = {}
    suits = ['S','H','D','C']

    spade = suits[0]
    spade_indices = [idx for idx in indices if idx.startswith(spade)]
    heart = suits[1]
    heart_indices = [idx for idx in indices if idx.startswith(heart)]
    diamond = suits[2]
    diamond_indices = [idx for idx in indices if idx.startswith(diamond)]
    club = suits[3]
    club_indices = [idx for idx in indices if idx.startswith(club)]
    print("calculate odds with same suits")
    for i in range(len(spade_indices)):
        for j in range(i + 1, len(spade_indices)):
            # Calculate odds for pairs within the same suit
            odds = calc.calculate(None, True, 1, None, [spade_indices[i], spade_indices[j], '?', '?'], False)
            odds_table[(spade_indices[i], spade_indices[j])] = odds
    # hearts
    for i in range(len(heart_indices)):
        for j in range(i+1, len(heart_indices)):
            odds_table[(heart_indices[i], heart_indices[j])] = odds_table[(spade_indices[i], spade_indices[j])]
    # diamonds
    for i in range(len(diamond_indices)):
        for j in range(i+1, len(diamond_indices)):
            odds_table[(diamond_indices[i], diamond_indices[j])] = odds_table[(spade_indices[i], spade_indices[j])]
    # clubs
    for i in range(len(club_indices)):
        for j in range(i+1, len(club_indices)):
            odds_table[(club_indices[i], club_indices[j])] = odds_table[(spade_indices[i], spade_indices[j])]
    # calculate the odds for all combinations that have suit S and suit H
    print("calculate odds with different suits")
    for i in range(len(spade_indices)):
        for j in range(len(heart_indices)):
            odds = calc.calculate(None, True, 1, None, [spade_indices[i], heart_indices[j], '?', '?'], False)
            odds_table[(spade_indices[i], heart_indices[j])] = odds
            odds_table[(heart_indices[j], spade_indices[i])] = odds
        for j in range(len(diamond_indices)):
            odds_table[(spade_indices[i], diamond_indices[j])] = odds_table[(spade_indices[i], heart_indices[j])]
            odds_table[(diamond_indices[j], spade_indices[i])] = odds_table[(heart_indices[j], spade_indices[i])]
        for j in range(len(club_indices)):
            odds_table[(spade_indices[i], club_indices[j])] = odds_table[(spade_indices[i], heart_indices[j])]
            odds_table[(club_indices[j], spade_indices[i])] = odds_table[(heart_indices[j], spade_indices[i])]
    for i in range(len(heart_indices)):
        for j in range(len(diamond_indices)):
            odds_table[(heart_indices[i], diamond_indices[j])] = odds_table[(spade_indices[i], heart_indices[j])]
            odds_table[(diamond_indices[j], heart_indices[i])] = odds_table[(heart_indices[j], spade_indices[i])]
        for j in range(len(club_indices)):
            odds_table[(heart_indices[i], club_indices[j])] = odds_table[(spade_indices[i], heart_indices[j])]
            odds_table[(club_indices[j], heart_indices[i])] = odds_table[(heart_indices[j], spade_indices[i])]
    for i in range(len(diamond_indices)):
        for j in range(len(club_indices)):
            odds_table[(diamond_indices[i], club_indices[j])] = odds_table[(spade_indices[i], heart_indices[j])]
            odds_table[(club_indices[j], diamond_indices[i])] = odds_table[(heart_indices[j], spade_indices[i])]
    return odds_table

def calculate_known_basedonSuit(indices):
    odds_table = {}
    suits = ['S','H','D','C']

    spade = suits[0]
    spade_indices = [idx for idx in indices if idx.startswith(spade)]
    heart = suits[1]
    heart_indices = [idx for idx in indices if idx.startswith(heart)]
    diamond = suits[2]
    diamond_indices = [idx for idx in indices if idx.startswith(diamond)]
    club = suits[3]
    club_indices = [idx for idx in indices if idx.startswith(club)]
    # first calculate the odds of all the cases where both players have cards from the same suit
    for i in range(len(spade_indices)):
        for j in range(i + 1, len(spade_indices)):
            for k in range(len(spade_indices)):
                for l in range(k + 1, len(spade_indices)):
                    # Ensure all entered cards are unique
                    if len(set([spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l]])) == 4:
                        odds = calc.calculate(None, True, 1, None, [spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l]], False)
                        odds_table[(spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l])] = odds
                        odds_table[(spade_indices[j], spade_indices[i], spade_indices[l], spade_indices[k])] = odds
                        odds_table[(spade_indices[k], spade_indices[l], spade_indices[i], spade_indices[j])] = odds
                        odds_table[(spade_indices[l], spade_indices[k], spade_indices[j], spade_indices[i])] = odds
    # now copy those odds for the other indices
    for i in range(len(heart_indices)):
        for j in range(i + 1, len(heart_indices)):
            for k in range(len(heart_indices)):
                for l in range(k + 1, len(heart_indices)):
                    odds_table[(heart_indices[i], heart_indices[j], heart_indices[k], heart_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l])]
    for i in range(len(diamond_indices)):
        for j in range(i + 1, len(diamond_indices)):
            for k in range(len(diamond_indices)):
                for l in range(k + 1, len(diamond_indices)):
                    odds_table[(diamond_indices[i], diamond_indices[j], diamond_indices[k], diamond_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l])]
    for i in range(len(club_indices)):
        for j in range(i + 1, len(club_indices)):
            for k in range(len(club_indices)):
                for l in range(k + 1, len(club_indices)):
                    odds_table[(club_indices[i], club_indices[j], club_indices[k], club_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], spade_indices[k], spade_indices[l])]
    # now calculate the odds for all combinations where both players have cards from the same suit but the suit between players differs
    for i in range(len(spade_indices)):
        for j in range(len(spade_indices)):
            for k in range(len(heart_indices)):
                for l in range(len(heart_indices)):
                    odds = calc.calculate(None, True, 1, None, [spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l]], False)
                    odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])] = odds
                    odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])] = odds
                    odds_table[(spade_indices[j], spade_indices[i], heart_indices[l], heart_indices[k])] = odds
                    odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])] = odds
    # now copy those odds for the other suits
            for k in range(len(diamond_indices)):
                for l in range(len(diamond_indices)):
                    odds_table[(spade_indices[i], spade_indices[j], diamond_indices[k], diamond_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(diamond_indices[k], diamond_indices[l], spade_indices[i], spade_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])]
                    odds_table[(spade_indices[j], spade_indices[i], diamond_indices[l], diamond_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
                    odds_table[(diamond_indices[l], diamond_indices[k], spade_indices[j], spade_indices[i])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
            for k in range(len(club_indices)):
                for l in range(len(club_indices)):
                    odds_table[(spade_indices[i], spade_indices[j], club_indices[k], club_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(club_indices[k], club_indices[l], spade_indices[i], spade_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])]
                    odds_table[(spade_indices[j], spade_indices[i], club_indices[l], club_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
                    odds_table[(club_indices[l], club_indices[k], spade_indices[j], spade_indices[i])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
    for i in range(len(heart_indices)):
        for j in range(len(heart_indices)):
            for k in range(len(diamond_indices)):
                for l in range(len(diamond_indices)):
                    odds_table[(heart_indices[i], heart_indices[j], diamond_indices[k], diamond_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(diamond_indices[k], diamond_indices[l], heart_indices[i], heart_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])]
                    odds_table[(heart_indices[j], heart_indices[i], diamond_indices[l], diamond_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
                    odds_table[(diamond_indices[l], diamond_indices[k], heart_indices[j], heart_indices[i])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
            for k in range(len(club_indices)):
                for l in range(len(club_indices)):
                    odds_table[(heart_indices[i], heart_indices[j], club_indices[k], club_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(club_indices[k], club_indices[l], heart_indices[i], heart_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])]
                    odds_table[(heart_indices[j], heart_indices[i], club_indices[l], club_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
                    odds_table[(club_indices[l], club_indices[k], heart_indices[j], heart_indices[i])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
    for i in range(len(diamond_indices)):
        for j in range(len(diamond_indices)):
            for k in range(len(club_indices)):
                for l in range(len(club_indices)):
                    odds_table[(diamond_indices[i], diamond_indices[j], club_indices[k], club_indices[l])] = odds_table[(spade_indices[i], spade_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(club_indices[k], club_indices[l], diamond_indices[i], diamond_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], spade_indices[j])]
                    odds_table[(diamond_indices[j], diamond_indices[i], club_indices[l], club_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
                    odds_table[(club_indices[l], club_indices[k], diamond_indices[j], diamond_indices[i])] = odds_table[(heart_indices[l], heart_indices[k], spade_indices[j], spade_indices[i])]
    # calculate the odds where the first player has cards from two different suits and the second player has cards from the same suit
    for i in range(len(spade_indices)):
        for j in range(len(heart_indices)):
            for k in range(len(heart_indices)):
                for l in range(len(heart_indices)):
                    odds = calc.calculate(None, True, 1, None, [spade_indices[i], heart_indices[j], heart_indices[k], heart_indices[l]], False)
                    odds_table[(spade_indices[i], heart_indices[j], heart_indices[k], heart_indices[l])] = odds
                    odds_table[(heart_indices[j], heart_indices[k], heart_indices[l], spade_indices[i])] = odds
                    odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], heart_indices[j])] = odds
                    odds_table[(heart_indices[l], spade_indices[i], heart_indices[j], heart_indices[k])] = odds
            # player has cards from different suits and opponents has card from same suit where the suit differs from the players suits
            for k in range(len(diamond_indices)):
                for l in range(len(diamond_indices)):
                    odds = calc.calculate(None, True, 1, None, [spade_indices[i], heart_indices[j], diamond_indices[k], diamond_indices[l]], False)
                    odds_table[(spade_indices[i], heart_indices[j], diamond_indices[k], diamond_indices[l])] = odds
                    odds_table[(diamond_indices[k], diamond_indices[l], spade_indices[i], heart_indices[j])] = odds
                    odds_table[(heart_indices[j], heart_indices[k], diamond_indices[l], diamond_indices[k])] = odds
                    odds_table[(diamond_indices[l], diamond_indices[k], heart_indices[j], heart_indices[k])] = odds



def calculate_known_oddstable(indices):
    # calculate the odds with both your hand and the opponent's hand known
    odds_table = {}
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            for k in range(len(indices)):
                for l in range(k + 1, len(indices)):
                    # Ensure all entered cards are unique
                    if len(set([indices[i], indices[j], indices[k], indices[l]])) == 4:
                        odds = calc.calculate(None, True, 1, None, [indices[i], indices[j], indices[k], indices[l]], False)
                        odds_table[(indices[i], indices[j], indices[k], indices[l])] = odds
                        print(f'{indices[i]}, {indices[j]}, {indices[k]}, {indices[l]}: {odds}')
    return odds_table


def classificationTable(indices):
    odds_table = {}
    # defining the ranks, s means they have the same suit o means they have a different suit, the letters and values are the values of the card
    # rank 1: AA, KK, AKs, QQ, JJ all get odds = 0.90
    # rank 2: TT, AQs, AJs, KQs, AKo all get odds = 0.80
    # rank 3: 99, JTs, QJs, KJs, ATs, AQo all get odds = 0.70
    # rank 4: 88, KTs, QTs, J9s, T9s, 98s, AJo, KQo all get odds = 0.60
    # rank 5: 77, A9s, A8s, A7s, A6s, A5s, A4s, A3s, A2s, Q9s, T8s, 97s, 87s, 76s, KJo, QJo, JTo all get odds = 0.50
    # rank 6: 66, 55, K9s, J8s, 86s, 75s, 54s, ATo, KTo, QTo all get odds = 0.40
    # rank 7: 44, 33, 22, K8s, K7s, K6s, K5s, K4s, K3s, K2s, Q8s, T7s, 64s, 53s, 43s, J9o, T9o, 98o all get odds = 0.30
    # rank 8: J7s, 96s, 85s, 74s, 42s, 32s, A9o, K9o, Q9o, J8o, T8o, 87o, 76o, 65o, 54o all get odds = 0.20
    # rank 9: all others get odds = 0.10
    # now we need to implement above ranks in a dictionary
    for i in range(len(indices)):
        for j in range(len(indices)):
            if not indices[i] == indices[j]:
                # make rank 1
                if indices[i][0] == indices[j][0] and indices[i][1] in ['A','K'] and indices[j][1] in ['A','K']:
                    odds_table[(indices[i], indices[j])] = 0.90
                elif indices[i][0] != indices[j][0] and indices[i][1] == indices[j][1] and indices[i][1] in ['A','K','Q','J'] and indices[j][1] in ['A','K','Q','J']:
                    odds_table[(indices[i], indices[j])] = 0.90
                elif indices[i][0] == indices[j][0]:
                    # make rank 2
                    if (indices[i][1] == 'A' or indices[j][1] == 'A') and (indices[i][1] in ['Q', 'J'] or indices[j][1] in ['Q', 'J']):
                        odds_table[(indices[i], indices[j])] = 0.80
                    elif indices[i][1] in ['Q', 'K'] and indices[j][1] in ['Q', 'K']:
                        odds_table[(indices[i], indices[j])] = 0.80
                    # make rank 3
                    elif (indices[i][1] == 'A' or indices[j][1] == 'A') and (indices[i][1] == 'T' or indices[j][1] == 'T'):
                        odds_table[(indices[i], indices[j])] = 0.70
                    elif (indices[i][1] == 'J' or indices[j][1] == 'J') and (indices[i][1] in ['T', 'K','Q'] or indices[j][1] in ['T', 'K','Q']):
                        odds_table[(indices[i], indices[j])] = 0.70
                    # make rank 4
                    elif (indices[i][1] == 'T' or indices[j][1] == 'T') and (indices[i][1] in ['9', 'K', 'Q'] or indices[j][1] in ['9', 'K', 'Q']):
                        odds_table[(indices[i], indices[j])] = 0.60
                    elif (indices[i][1] == '9' or indices[j][1] == '9') and (indices[i][1] in ['J', '8'] or indices[j][1] in ['J', '8']):
                        odds_table[(indices[i], indices[j])] = 0.60
                    # make rank 5
                    elif (indices[i][1] == 'A' or indices[j][1] == 'A') and (indices[i][1] in ['9', '8', '7', '6', '5', '4', '3', '2'] or indices[j][1] in ['9', '8', '7', '6', '5', '4', '3', '2']):
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif (indices[i][1] == '7' or indices[j][1] == '7') and (indices[i][1] in ['9', '8', '6'] or indices[j][1] in ['9', '8', '6']):
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif indices[i][1] in ['8', 'T'] and indices[j][1] in ['8', 'T']:
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif indices[i][1] in ['Q', '9'] and indices[j][1] in ['Q', '9']:
                        odds_table[(indices[i], indices[j])] = 0.50
                    # make rank 6
                    elif (indices[i][1] == '8' or indices[i][1] == '8') and (indices[i][1] in ['J', '6'] or indices[j][1] in ['J', '6']):
                        odds_table[(indices[i], indices[j])] = 0.40
                    elif (indices[i][1] == '5' or indices[i][1] == '5') and (indices[i][1] in ['4', '7'] or indices[j][1] in ['4', '7']):
                        odds_table[(indices[i], indices[j])] = 0.40
                    elif indices[i][1] in ['K', '9'] and indices[j][1] in ['K', '9']:
                        odds_table[(indices[i], indices[j])] = 0.40
                    # make rank 7
                    elif (indices[i][1] == 'K' or indices[j][1] == 'K') and (indices[i][1] in ['2', '3', '4', '5', '6', '7', '8'] or indices[j][1] in ['2', '3', '4', '5', '6', '7', '8']):
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif (indices[i][1] == '3' or indices[j][1] == '3') and (indices[i][1] in ['4', '5'] or indices[j][1] in ['4', '5']):
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] in ['Q', '8'] and indices[j][1] in ['Q', '8']:
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] in ['T', '7'] and indices[j][1] in ['T', '7']:
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] in ['6', '4'] and indices[j][1] in ['6', '4']:
                        odds_table[(indices[i], indices[j])] = 0.30
                    # make rank 8
                    elif (indices[i][1] == '2' or indices[j][1] == '2') and (indices[i][1] in ['3', '4'] or indices[j][1] in ['3', '4']):
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif (indices[i][1] == '7' or indices[j][1] == '7') and (indices[i][1] in ['J', '4'] or indices[j][1] in ['J', '4']):
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif indices[i][1] in ['9', '6'] and indices[j][1] in ['9', '6']:
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif indices[i][1] in ['8', '5'] and indices[j][1] in ['8', '5']:
                        odds_table[(indices[i], indices[j])] = 0.20
                    else:
                        odds_table[(indices[i], indices[j])] = 0.10
                elif indices[i][0] != indices[j][0]:
                    # make rank 2
                    if (indices[i][1] in ['A', 'K'] and indices[j][1] in ['A', 'K']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.80
                    elif indices[i][1] == 'T' and indices[j][1] == 'T':
                        odds_table[(indices[i], indices[j])] = 0.80
                    # make rank 3
                    elif (indices[i][1] in ['A', 'Q'] and indices[j][1] in ['A', 'Q']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.70
                    elif indices[i][1] == '9' and indices[j][1] == '9':
                        odds_table[(indices[i], indices[j])] = 0.70
                    # make rank 4
                    elif (indices[i][1] in ['A', 'J'] and indices[j][1] in ['A', 'J']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.60
                    elif (indices[i][1] in ['K', 'Q'] and indices[j][1] in ['K', 'Q']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.60
                    elif indices[i][1] == '8' and indices[j][1] == '8':
                        odds_table[(indices[i], indices[j])] = 0.60
                    # make rank 5
                    elif (indices[i][1] in ['K', 'J'] and indices[j][1] in ['K', 'J']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif (indices[i][1] in ['J', 'Q'] and indices[j][1] in ['J', 'Q']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif (indices[i][1] in ['J', 'T'] and indices[j][1] in ['J', 'T']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.50
                    elif indices[i][1] == '7' and indices[j][1] == '7':
                        odds_table[(indices[i], indices[j])] = 0.50
                    # make rank 6
                    elif (indices[i][1] == 'T' or indices[j][1] == 'T') and (indices[i][1] in ['A', 'K', 'Q'] or indices[j][1] in ['A', 'K', 'Q']):
                        odds_table[(indices[i], indices[j])] = 0.40
                    elif indices[i][1] == '5' and indices[j][1] == '5':
                        odds_table[(indices[i], indices[j])] = 0.40
                    elif indices[i][1] == '6' and indices[j][1] == '6':
                        odds_table[(indices[i], indices[j])] = 0.40
                    # make rank 7
                    elif (indices[i][1] == '9' or indices[j][1] == '9') and (indices[i][1] in ['J', 'T', '8'] or indices[j][1] in ['J', 'T', '8']):
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] == '4' and indices[j][1] == '4':
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] == '3' and indices[j][1] == '3':
                        odds_table[(indices[i], indices[j])] = 0.30
                    elif indices[i][1] == '2' and indices[j][1] == '2':
                        odds_table[(indices[i], indices[j])] = 0.30
                    # make rank 8
                    elif (indices[i][1] == '9' or indices[j][1] == '9') and (indices[i][1] in ['A', 'K', 'Q'] or indices[j][1] in ['A', 'K', 'Q']):
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif (indices[i][1] == '8' or indices[j][1] == '8') and (indices[i][1] in ['J', 'T', '7'] or indices[j][1] in ['J', 'T', '7']):
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif (indices[i][1] == '6' or indices[j][1] == '6') and (indices[i][1] in ['7', '5'] or indices[j][1] in ['7', '5']):
                        odds_table[(indices[i], indices[j])] = 0.20
                    elif (indices[i][1] in ['5', '4'] and indices[j][1] in ['5', '4']) and indices[i][1] != indices[j][1]:
                        odds_table[(indices[i], indices[j])] = 0.20
                    else:
                        odds_table[(indices[i], indices[j])] = 0.10
    return odds_table

if __name__ == '__main__':
    cards = rlcard.utils.utils.init_standard_deck()  # Initialize a standard deck of 52 cards
    indices = [card.get_index() for card in cards]  # Get the index of a card
    print(indices)
    odds_table = classificationTable(indices)
    with open('classification_table.json', 'w') as file:
        # Convert keys from tuples to strings
        string_keys_table = {str(key): value for key, value in odds_table.items()}
        json.dump(string_keys_table, file)

    with open('classification_table.json', 'r') as file:
        table = json.load(file)
        table = {eval(key): value for key, value in table.items()}
    print(table[('H6', 'D6')])
   #semiknown_table = calculate_semiknown_basedonSuit(indices)
 #   known_table = calculate_known_oddstable(indices)

    #with open('semiknown_table.json', 'w') as file:
    #    json.dump(semiknown_table, file)

    # with open('known_table.json', 'w') as file:
    #     json.dump(known_table, file)
