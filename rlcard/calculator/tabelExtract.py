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
                    odds_table[(spade_indices[i], heart_indices[j], diamond_indices[k], diamond_indices[l])] = odds_table[(spade_indices[i], heart_indices[j], heart_indices[k], heart_indices[l])]
                    odds_table[(diamond_indices[k], diamond_indices[l], spade_indices[i], heart_indices[j])] = odds_table[(heart_indices[k], heart_indices[l], spade_indices[i], heart_indices[j])]
                    odds_table[(heart_indices[j], heart_indices[k], diamond_indices[l], diamond_indices[k])] = odds_table[(heart_indices[j], heart_indices[k], heart_indices[l], heart_indices[k])]
                    odds_table[(diamond_indices[l], diamond_indices[k], heart_indices[j], heart_indices[k])] = odds_table[(heart_indices[l], heart_indices[k], heart_indices[j], heart_indices[k])]



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


if __name__ == '__main__':
    cards = rlcard.utils.utils.init_standard_deck()  # Initialize a standard deck of 52 cards
    indices = [card.get_index() for card in cards]  # Get the index of a card
    semiknown_table = calculate_semiknown_basedonSuit(indices)
 #   known_table = calculate_known_oddstable(indices)

    with open('semiknown_table.json', 'w') as file:
        json.dump(semiknown_table, file)

    # with open('known_table.json', 'w') as file:
    #     json.dump(known_table, file)
