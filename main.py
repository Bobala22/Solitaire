import pygame
from pygame.locals import *
import sys
import random

#################### Screen Setup ####################
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_color = pygame.Color(53, 162, 72)
display_surf.fill(bg_color)

# display positions
card_width = 81
card_height = 106

tableau_width_pos = 200
tableau_height_pos = 200

talon_width_pos = 150
talon_height_pos = 50

stock_width_pos = 50
stock_height_pos = 50

foundations_width_pos = 400
foundations_height_pos = 50

#######################################################

back_of_card = "deck-of-cards/Back8.png"
card_images = {}
back_image = pygame.image.load(back_of_card)
back_image = pygame.transform.scale(back_image, (card_width, card_height))
deck_of_cards = []

tableau = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
foundations = {'hearts': [], 'diamonds': [], 'clubs': [], 'spades': []}
stock = []
talon = []

bg_color = pygame.Color(53, 162, 72)
button_color = (255, 255, 255)
button_hover_color = (200, 200, 200)
text_color = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Button positions
easy_button_rect = pygame.Rect(350, 250, 300, 100)
hard_button_rect = pygame.Rect(350, 400, 300, 100)

dragging = False
drag_card = []
drag_from = None
drag_offset = (0, 0)
drag_pos = (0, 0)

def load_card_images():
    global card_images
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        if suit == 'hearts': number = 2
        elif suit == 'diamonds': number = 4
        elif suit == 'clubs': number = 7
        elif suit == 'spades': number = 5
        
        for value in range(1, 14):
            if value == 1: sign = 'A'
            elif value == 11: sign = 'J'
            elif value == 12: sign = 'Q'
            elif value == 13: sign = 'K'
            else: sign = str(value)
            
            img_path = 'deck-of-cards/' + sign + "." + str(number) + '.png'
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (card_width, card_height))
            card_images[(value, suit)] = img
            deck_of_cards.append((value, suit, False))

def draw_intro_screen():
    display_surf.fill(bg_color)

    title_text = font.render("Solitaire", True, text_color)
    subtitle_text = button_font.render("Choose your difficulty", True, text_color)
    
    display_surf.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    display_surf.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150))
    
    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    
    if easy_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display_surf, button_hover_color, easy_button_rect, border_radius=20)
    else:
        pygame.draw.rect(display_surf, button_color, easy_button_rect, border_radius=20)
    
    if hard_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display_surf, button_hover_color, hard_button_rect, border_radius=20)
    else:
        pygame.draw.rect(display_surf, button_color, hard_button_rect, border_radius=20)
    
    # Draw text
    easy_text = button_font.render("Easy Game", True, text_color)
    hard_text = button_font.render("Hard Game", True, text_color)
    
    display_surf.blit(easy_text, (easy_button_rect.x + 50, easy_button_rect.y + 25))
    display_surf.blit(hard_text, (hard_button_rect.x + 50, hard_button_rect.y + 25))
    
    pygame.display.flip()

def deal():
    for i in range(1, 8):
        for j in range(i):
            card = deck_of_cards.pop(0)
            if j == i - 1:
                card = (card[0], card[1], True)
                tableau[i].append(card)
            else:
                tableau[i].append(card)
    for i in range(24):
        stock.append(deck_of_cards.pop(0))

def draw_tableau():
    x_offset = tableau_width_pos
    y_offset = tableau_height_pos
    global card_positions
    card_positions = {}
    for key in tableau:
        x = x_offset + (int(key) - 1) * 100
        y = y_offset
        if tableau[key] == []:
            rect = pygame.Rect(x, y, card_width, card_height)
            pygame.draw.rect(display_surf, (255, 255, 255), rect, border_radius=10, width=2)
        else:
            for index, card in enumerate(tableau[key]):
                if card[2]:  # card face up
                    display_surf.blit(card_images[(card[0], card[1])], (x, y))
                else:  # card face down
                    display_surf.blit(back_image, (x, y))
                card_rect = pygame.Rect(x, y, card_width, card_height)
                card_positions[(key, index)] = card_rect
                y += 30

def draw_stock():
    if stock:
        x = stock_width_pos
        y = stock_height_pos
        display_surf.blit(back_image, (x, y))

def draw_foundations():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    for i, suit in enumerate(suits):
        x = foundations_width_pos + i * 100
        y = foundations_height_pos
        if foundations[suit]:
            card = foundations[suit][-1]
            display_surf.blit(card_images[(card[0], card[1])], (x, y))
        else:
            rect = pygame.Rect(x, y, card_width, card_height)
            pygame.draw.rect(display_surf, (255, 255, 255), rect, border_radius=10, width=2)

def is_opposite_color(suit1, suit2):
    red_suits = ['hearts', 'diamonds']
    black_suits = ['clubs', 'spades']
    return (suit1 in red_suits and suit2 in black_suits) or (suit1 in black_suits and suit2 in red_suits)

def can_place_on_tableau(target_pile, card):
    if not target_pile:
        return card[0] == 13 # only K on empty tableau
    top_card = target_pile[-1]
    if not top_card[2]:  # Face-down card
        return False
    return is_opposite_color(top_card[1], card[1]) and card[0] == top_card[0] - 1

def can_place_on_foundation(foundation_pile, card):
    if not foundation_pile:
        return card[0] == 1  # only A on empty foundation
    top_card = foundation_pile[-1]
    return card[1] == top_card[1] and card[0] == top_card[0] + 1

def win_game():
    for key in foundations:
        if len(foundations[key]) != 13:
            return False
    return True

def remove_card():
    global stock
    for card1 in cards_to_remove:
        for card11 in card1:
            for card2 in stock:
                if card11[0] == card2[0] and card11[1] == card2[1]:
                        stock.remove(card11)
                        break
                
def draw_win_screen():
    title_text = font.render("You Win!", True, text_color)
    display_surf.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    pygame.display.flip()

def can_move_to_foundations(card):
    foundation_pile = foundations[card[1]]
    return can_place_on_foundation(foundation_pile, card)

def can_place_sequence_on_tableau(dest_pile, sequence):
    if not sequence:
        return False
    first_card = sequence[0]
    return can_place_on_tableau(dest_pile, first_card)


def start_game(difficulty):
    global dragging, drag_card, drag_from, drag_offset, drag_pos

    if difficulty == "easy":
        talon_drag = 1
        def draw_talon():
            global talon_positions
            talon_positions = []
            x = talon_width_pos
            y = talon_height_pos
            card = talon[0]
            display_surf.blit(card_images[(card[0], card[1])], (x, y))
            card_rect = pygame.Rect(x, y, card_width, card_height)
            talon_positions.append(card_rect)

        def draw_from_stock():
            global talon, stock
            if 50 <= mouse_pos[0] <= 121 and 50 <= mouse_pos[1] <= 146:
                talon.clear()
                talon = stock[-1:]
                for i in range(len(talon)):
                    card = talon[i]
                    talon[i] = (card[0], card[1], True)
                stock = stock[:-1]
                stock = talon + stock
                remove_card()

    elif difficulty == "hard":
        talon_drag = 3
        def draw_talon():
            global talon_positions
            talon_positions = []
            x = talon_width_pos
            y = talon_height_pos
            overlap = 20
            for i, card in enumerate(talon):
                card_x = x + (i * overlap)
                display_surf.blit(card_images[(card[0], card[1])], (card_x, y))
                card_rect = pygame.Rect(card_x, y, card_width, card_height)
                talon_positions.append(card_rect)

        def draw_from_stock():
            global talon, stock
            if 50 <= mouse_pos[0] <= 121 and 50 <= mouse_pos[1] <= 146:
                talon.clear()
                talon = stock[-3:]
                for i in range(len(talon)):
                    card = talon[i]
                    talon[i] = (card[0], card[1], True)
                stock = stock[:-3]
                stock = talon + stock
                remove_card()

    while True:
        if win_game():
            draw_win_screen()
        display_surf.fill(bg_color)
        draw_tableau()
        draw_stock()
        draw_foundations()
        if talon:
            draw_talon()
        if dragging:
            y_offset = 0
            for card in drag_card:
                display_surf.blit(card_images[(card[0], card[1])], (drag_pos[0], drag_pos[1] + y_offset))
                y_offset += 30

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # draw from the stock
                draw_from_stock()

                # drag from talon
                if talon:
                    for index, rect in enumerate(reversed(talon_positions)):
                        if rect.collidepoint(mouse_pos):
                            dragging = True
                            drag_card = [talon.pop(index-1)]
                            drag_from = ('talon', index)
                            drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                            drag_pos = (rect.x, rect.y)
                            talon_drag -= 1
                            break
                
                # drag from foundations
                for key in foundations:
                    if foundations[key]:
                        rect = pygame.Rect(foundations_width_pos + (list(foundations.keys()).index(key)) * 100, foundations_height_pos, card_width, card_height)
                        if rect.collidepoint(mouse_pos):
                            dragging = True
                            drag_card = [foundations[key].pop()]
                            drag_from = ('foundations', key)
                            drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                            drag_pos = (rect.x, rect.y)
                            break

                # drag from tablaeu
                for key in tableau:
                    for index in range(len(tableau[key]) - 1, -1, -1):
                        card = tableau[key][index]
                        if card[2]:  # Face-up card
                            rect = card_positions[(key, index)]
                            if rect.collidepoint(mouse_pos):
                                dragging = True
                                drag_card = tableau[key][index:]
                                drag_from = ('tableau', (key, index))
                                drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                                drag_pos = (rect.x, rect.y)
                                tableau[key] = tableau[key][:index]
                                break
                    if dragging:
                        break

            if event.type == MOUSEMOTION and dragging:
                mouse_pos = pygame.mouse.get_pos()
                drag_pos = (mouse_pos[0] - drag_offset[0], mouse_pos[1] - drag_offset[1])

            if event.type == MOUSEBUTTONUP and dragging:
                mouse_pos = pygame.mouse.get_pos()
                placed = False

                # try to place on tableau
                if not placed:
                    for key in tableau:
                        pile_x = tableau_width_pos + (int(key) - 1) * 100
                        last_card_y = tableau_height_pos + (len(tableau[key]) - 1) * 20  # Adjust offset as needed
                        last_card_rect = pygame.Rect(pile_x+20, last_card_y+20, card_width+20, card_height+20)
                        if last_card_rect.collidepoint(mouse_pos):
                            if can_place_on_tableau(tableau[key], drag_card[0]):
                                tableau[key].extend(drag_card)
                                placed = True
                                if 'talon' in drag_from:
                                    cards_to_remove.append(drag_card)
                                if 'tableau' in drag_from:
                                    if tableau[drag_from[1][0]]:
                                        tableau[drag_from[1][0]][-1] = (
                                            tableau[drag_from[1][0]][-1][0],
                                            tableau[drag_from[1][0]][-1][1],
                                            True
                                        )
                                    else:
                                        tableau[drag_from[1][0]] = []
                            break
                       
                # try to place on foundation
                if not placed:
                    if len(drag_card) == 1:
                        suits = ['hearts', 'diamonds', 'clubs', 'spades']
                        for i, suit in enumerate(suits):
                            x = foundations_width_pos + i * 100
                            y = foundations_height_pos
                            found_rect = pygame.Rect(x, y, card_width, card_height)
                            if found_rect.collidepoint(mouse_pos):
                                if can_place_on_foundation(foundations[suit], drag_card[0]):
                                    foundations[suit].append(drag_card[0])
                                    placed = True
                                    if 'talon' in drag_from:
                                        cards_to_remove.append(drag_card)
                                    if 'tableau' in drag_from:
                                        if tableau[drag_from[1][0]]:
                                            tableau[drag_from[1][0]][-1] = (tableau[drag_from[1][0]][-1][0], tableau[drag_from[1][0]][-1][1], True)
                                        else:
                                            tableau[drag_from[1][0]] = []

                if not placed:
                    if drag_from[0] == 'talon':
                        talon.append(drag_card[0])
                        talon_drag += 1
                    elif drag_from[0] == 'tableau':
                        tableau[drag_from[1][0]].extend(drag_card)
                    elif drag_from[0] == 'foundations':
                        foundations[drag_from[1]].append(drag_card[0])

                dragging = False
                drag_card = []
                drag_from = None

        pygame.display.update()
        FramePerSec.tick(FPS)

def main():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button_rect.collidepoint(mouse_pos):
                    intro = False
                    start_game("easy")
                elif hard_button_rect.collidepoint(mouse_pos):
                    intro = False
                    start_game("hard")
        
        draw_intro_screen()
        pygame.display.update()

if __name__ == "__main__":
    load_card_images()
    random.shuffle(deck_of_cards)
    deal()

    talon_positions = []
    cards_to_remove = []

    main()