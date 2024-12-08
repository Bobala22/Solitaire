import pygame
from pygame.locals import *
import sys
import random

#################### Screen Setup ####################
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_color = pygame.Color(53, 162, 72)
display_surf.fill(bg_color)

#######################################################

back_of_card = "deck-of-cards/Back8.png"
card_images = {}
back_image = pygame.image.load(back_of_card)
back_image = pygame.transform.scale(back_image, (71, 96))

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
            img = pygame.transform.scale(img, (71, 96))
            card_images[(value, suit)] = img

deck_of_cards = []
for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
    if suit == 'hearts':
        number = 2
    elif suit == 'diamonds':
        number = 4
    elif suit == 'clubs':
        number = 7
    elif suit == 'spades':
        number = 5
    for value in range(1, 14):
        if value == 1:
            sign = 'A'
        elif value == 11:
            sign = 'J'
        elif value == 12:
            sign = 'Q'
        elif value == 13:
            sign = 'K'
        else:
            sign = str(value)
        img_path = 'deck-of-cards/' + sign + "." + str(number) + '.png'
        deck_of_cards.append((value, suit, img_path, False))

random.shuffle(deck_of_cards)

tableau = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': []}
foundations = {'hearts': [], 'diamonds': [], 'clubs': [], 'spades': []}
stock = []
talon = []

def deal():
    for i in range(1, 8):
        for j in range(i):
            tableau[str(i)].append(deck_of_cards.pop(0))
            if j == i - 1:
                tableau[str(i)][j] = (tableau[str(i)][j][0], tableau[str(i)][j][1], tableau[str(i)][j][2], True)
            else:
                tableau[str(i)][j] = (tableau[str(i)][j][0], tableau[str(i)][j][1], tableau[str(i)][j][2], False)
    for i in range(24):
        stock.append(deck_of_cards.pop(0))

def draw_tableau():
    x_offset = 200
    y_offset = 200
    for key in tableau:
        x = x_offset + (int(key) - 1) * 100
        y = y_offset
        for card in tableau[key]:
            if card[3]:  # card face up
                display_surf.blit(card_images[(card[0], card[1])], (x, y))
            else:  # card face down
                display_surf.blit(back_image, (x, y))
            y += 30

def draw_talon():
    x = 150
    y = 50
    overlap = 20
    
    for i, card in enumerate(talon[-3:]):
        display_surf.blit(card_images[(card[0], card[1])], (x + (i * overlap), y))

def draw_stock():
    if stock:
        x = 50
        y = 50
        display_surf.blit(back_image, (x, y))

def draw_foundations():
    x_offset = 400
    y_offset = 50
    rect_size = (71, 96)
    for i in range(4):
        rect = pygame.Rect(x_offset + i * 100, y_offset, rect_size[0], rect_size[1])
        pygame.draw.rect(display_surf, (255, 255, 255), rect, border_radius=10, width=2)  # 2 is the border width

load_card_images()
deal()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 50 <= mouse_pos[0] <= 121 and 50 <= mouse_pos[1] <= 146:
                if stock:
                    for _ in range(min(3, len(stock))):
                        card = stock.pop()
                        talon.append((card[0], card[1], card[2], True))
                elif not stock and talon:
                    while talon:
                        card = talon.pop()
                        stock.append((card[0], card[1], card[2], False))

    display_surf.fill(bg_color)
    draw_tableau()
    draw_stock()
    draw_foundations()
    if talon:
        draw_talon()

    pygame.display.update()
    FramePerSec.tick(FPS)