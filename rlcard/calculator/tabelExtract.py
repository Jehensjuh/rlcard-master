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



def calculate_known_oddstable(indices):
    # calculate the odds with both your hand and the opponent's hand known
    odds_table = {}
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            for k in range(len(indices)):
                for l in range(k + 1, len(indices)):
                    odds = calc.calculate(None, True, 1, None, [indices[i], indices[j], indices[k], indices[l]], False)
                    odds_table[(indices[i], indices[j], indices[k], indices[l])] = odds
                    print(f'{indices[i]}, {indices[j]}, {indices[k]}, {indices[l]}: {odds}')

if __name__ == '__main__':
    cards = rlcard.utils.utils.init_standard_deck()  # Initialize a standard deck of 52 cards
    indices = [card.get_index() for card in cards]  # Get the index of a card
    # semiknown_table = calculate_semiknown_oddstable(indices)
    known_table = calculate_known_oddstable(indices)

 #   with open('semiknown_table.json', 'w') as file:
 #       json.dump(semiknown_table, file)

    with open('known_table.json', 'w') as file:
        json.dump(known_table, file)
