## Script pt. a elimina sprite-urile pe care nu le folosesc din pachetul deck-of-cards

import os
for card in os.listdir('deck-of-cards'):
   if card.startswith('Back') == False:
    if card[2] == '1' or card[2] == '3' or card[2] == '6' or card[2] == '8':
        os.remove('deck-of-cards/' + card)