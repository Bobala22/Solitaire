import pygame
from pygame.locals import *
import sys
import random

#################### Screen Setup ####################
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()

TIMER_FONT = pygame.font.Font(None, 36)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG_COLOR = pygame.Color(53, 162, 72)
display_surf.fill(BG_COLOR)

# display positions
CARD_WIDTH = 81
CARD_HEIGHT = 106

TABLEAU_WIDTH_POS = 200
TABLEAU_HEIGHT_POS = 200

TALON_WIDTH_POS = 150
TALON_HEIGHT_POS = 50

STOCK_WIDTH_POS = 50
STOCK_HEIGHT_POS = 50

FOUNDATIONS_WIDTH_POS = 400
FOUNDATIONS_HEIGHT_POS = 50

#######################################################

back_of_card = "deck-of-cards/Back8.png"
card_images = {}
back_image = pygame.image.load(back_of_card)
back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
deck_of_cards = []
new_game_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 140, 50)

tableau = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
foundations = {"hearts": [], "diamonds": [], "clubs": [], "spades": []}
stock = []
talon = []

BG_COLOR = pygame.Color(53, 162, 72)
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

def draw_timer():
    """
    Function used to draw the timer on the screen. It will display the elapsed time since the game started.
    """
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = TIMER_FONT.render(f"Time: {minutes:02}:{seconds:02}", True, text_color)
    display_surf.blit(timer_text, (SCREEN_WIDTH - 150, 10))

def load_card_images():
    """
    Load card images from the deck-of-cards folder and store them in a list - card_images.
    Prepare the whole deck of cards as a list with tuples (value, suit, face_up).
    """
    global card_images
    for suit in ["hearts", "diamonds", "clubs", "spades"]:
        if suit == "hearts":
            number = 2
        elif suit == "diamonds":
            number = 4
        elif suit == "clubs":
            number = 7
        elif suit == "spades":
            number = 5

        for value in range(1, 14):
            if value == 1:
                sign = "A"
            elif value == 11:
                sign = "J"
            elif value == 12:
                sign = "Q"
            elif value == 13:
                sign = "K"
            else:
                sign = str(value)

            img_path = "deck-of-cards/" + sign + "." + str(number) + ".png"
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
            card_images[(value, suit)] = img
            deck_of_cards.append((value, suit, False))


def draw_intro_screen():
    """
    Draw the menu screen with the title and buttons for choosing the difficulty (easy or hard).
    """
    display_surf.fill(BG_COLOR)

    title_text = font.render("Solitaire", True, text_color)
    subtitle_text = button_font.render("Choose your difficulty", True, text_color)

    display_surf.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    display_surf.blit(
        subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150)
    )

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()

    if easy_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            display_surf, button_hover_color, easy_button_rect, border_radius=20
        )
    else:
        pygame.draw.rect(display_surf, button_color, easy_button_rect, border_radius=20)

    if hard_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            display_surf, button_hover_color, hard_button_rect, border_radius=20
        )
    else:
        pygame.draw.rect(display_surf, button_color, hard_button_rect, border_radius=20)

    # Draw text
    easy_text = button_font.render("Easy Game", True, text_color)
    hard_text = button_font.render("Hard Game", True, text_color)

    display_surf.blit(easy_text, (easy_button_rect.x + 50, easy_button_rect.y + 25))
    display_surf.blit(hard_text, (hard_button_rect.x + 50, hard_button_rect.y + 25))

    pygame.display.flip()


def deal():
    """
    Deal the cards to the tableau and stock piles. The rules of this distribution can be checked in the Rules secion in the README.md file.

    The last card of each tableau pile is face up, the rest are face down.
    There will be 7 tableau piles, each with a different number of cards. 
    The first pile will have 1 card, the second 2 cards, and so on, up to the seventh pile with 7 cards.

    The rest of the cards will be placed in the stock pile.
    """
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
    """
    Draw the tableau piles with the cards. If the pile is empty, draw a white rectangle with a border, to indicate the position of an empty pile.
    """
    x_offset = TABLEAU_WIDTH_POS
    y_offset = TABLEAU_HEIGHT_POS
    global card_positions
    card_positions = {}
    for key in tableau:
        x = x_offset + (int(key) - 1) * 100
        y = y_offset
        if tableau[key] == []:
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(
                display_surf, (255, 255, 255), rect, border_radius=10, width=2
            )
        else:
            for index, card in enumerate(tableau[key]):
                if card[2]:  # card face up
                    display_surf.blit(card_images[(card[0], card[1])], (x, y))
                else:  # card face down
                    display_surf.blit(back_image, (x, y))
                card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                card_positions[(key, index)] = card_rect
                y += 30


def draw_stock():
    """
    Draw the stock pile with the cards. If the pile is empty, draw a white rectangle with a border, to indicate the position of an empty pile.
    """
    if stock:
        x = STOCK_WIDTH_POS
        y = STOCK_HEIGHT_POS
        display_surf.blit(back_image, (x, y))
    else:
        rect = pygame.Rect(STOCK_WIDTH_POS, STOCK_HEIGHT_POS, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(
            display_surf, (255, 255, 255), rect, border_radius=10, width=2
        )


def draw_foundations():
    """
    Draw the foundation piles with the cards. If the pile is empty, draw a white rectangle with a border, to indicate the position of an empty pile.
    We have 4 foundation piles, one for each suit.
    """
    suits = ["hearts", "diamonds", "clubs", "spades"]
    for i, suit in enumerate(suits):
        x = FOUNDATIONS_WIDTH_POS + i * 100
        y = FOUNDATIONS_HEIGHT_POS
        if foundations[suit]:
            card = foundations[suit][-1]
            display_surf.blit(card_images[(card[0], card[1])], (x, y))
        else:
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(
                display_surf, (255, 255, 255), rect, border_radius=10, width=2
            )


def is_opposite_color(suit1, suit2):
    """
    Check if two suits are of opposite colors. We will use this when placing cards on the tableau piles. For more infomration, check the Rules section in the README.md file.
    """
    red_suits = ["hearts", "diamonds"]
    black_suits = ["clubs", "spades"]
    return (suit1 in red_suits and suit2 in black_suits) or (
        suit1 in black_suits and suit2 in red_suits
    )


def can_place_on_tableau(target_pile, card):
    """
    Function to check if a card can be placed on a tableau pile. 
    The card must be of the opposite color of the top card of the tableau pile and have a value one less than the top card.
    If the pile is empty, only a King can be placed on it.
    """
    if not target_pile:
        return card[0] == 13  # only K on empty tableau
    top_card = target_pile[-1]
    if not top_card[2]:  # Face-down card
        return False
    return is_opposite_color(top_card[1], card[1]) and card[0] == top_card[0] - 1


def can_place_on_foundation(foundation_pile, card):
    """
    Check if a card can be placed on a foundation pile. The card must be of the same suit as the top card of the foundation pile and have a value one greater than the top card.
    If the pile is empty, only an Ace can be placed on it.
    """
    if not foundation_pile:
        return card[0] == 1  # only A on empty foundation
    top_card = foundation_pile[-1]
    return card[1] == top_card[1] and card[0] == top_card[0] + 1


def win_game():
    """
    The game is won only when all the foundation piles have 13 cards each.
    """
    for key in foundations:
        if len(foundations[key]) != 13:
            return False
    return True


def remove_card():
    """
    This function is used to remove a card from the stock pile after it has been drawn and successfully placed on the tableau or foundation piles.
    """
    global stock
    for card1 in cards_to_remove:
        for card11 in card1:
            for card2 in stock:
                if card11[0] == card2[0] and card11[1] == card2[1]:
                    stock.remove(card11)
                    break

def draw_new_game_button():
    """
    Function to draw the new game button on the screen.
    """
    button_font = pygame.font.SysFont(None, 36)
    new_game_text = button_font.render("New Game", True, text_color)
    
    mouse_pos = pygame.mouse.get_pos()
    if new_game_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display_surf, (220, 220, 220), new_game_button_rect, border_radius=15)
    else:
        pygame.draw.rect(display_surf, (180, 180, 180), new_game_button_rect, border_radius=15)

    display_surf.blit(
        new_game_text,
        (
            new_game_button_rect.centerx - new_game_text.get_width() // 2,
            new_game_button_rect.centery - new_game_text.get_height() // 2
        )
    )

def check_new_game_button_click():
    """
    Function to check if the new game button has been clicked. If it has, the main menu will be displayed again.
    """
    global start_time, game_won
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_game_button_rect.collidepoint(event.pos):
                start_time = pygame.time.get_ticks()
                game_won = False
                main()

game_won = False

def draw_win_screen():
    """
    After the game is won, this function will display a message on the screen and provide buttons to play again or exit. 
    It will also display the best 3 times that have been achieved so far and save the current time.
    """
    global game_won, start_time
    elapsed_time = 0
    if not game_won:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Save the time to a file
        with open("best_times.txt", "a") as file:
            file.write(f"{elapsed_time}\n")

        game_won = True

    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_str = f"{minutes:02}:{seconds:02}"

    # Read the best 3 times
    with open("best_times.txt", "r") as file:
        times = [int(line.strip()) for line in file]
    best_times = sorted(times)[:3]

    display_surf.fill(BG_COLOR)
    title_text = font.render("You Win!", True, text_color)
    display_surf.blit(
        title_text,
        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50)
    )

    time_text = TIMER_FONT.render(f"Your Time: {time_str}", True, text_color)
    display_surf.blit(
        time_text,
        (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 100)
    )

    best_times_text = TIMER_FONT.render("Best Times:", True, text_color)
    display_surf.blit(
        best_times_text,
        (SCREEN_WIDTH // 2 - best_times_text.get_width() // 2, 150)
    )

    for i, best_time in enumerate(best_times):
        minutes = best_time // 60
        seconds = best_time % 60
        best_time_str = f"{minutes:02}:{seconds:02}"
        best_time_text = TIMER_FONT.render(f"{i + 1}. {best_time_str}", True, text_color)
        display_surf.blit(
            best_time_text,
            (SCREEN_WIDTH // 2 - best_time_text.get_width() // 2, 180 + i * 50)
        )

    button_font = pygame.font.SysFont(None, 36)
    play_again_text = button_font.render("Play Again", True, text_color)
    exit_text = button_font.render("Exit", True, text_color)

    play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 100)
    exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 100)

    mouse_pos = pygame.mouse.get_pos()

    if play_again_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display_surf, (220, 220, 220), play_again_button_rect, border_radius=15)
    else:
        pygame.draw.rect(display_surf, (180, 180, 180), play_again_button_rect, border_radius=15)

    display_surf.blit(
        play_again_text,
        (
            play_again_button_rect.centerx - play_again_text.get_width() // 2,
            play_again_button_rect.centery - play_again_text.get_height() // 2
        )
    )

    if exit_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display_surf, (220, 220, 220), exit_button_rect, border_radius=15)
    else:
        pygame.draw.rect(display_surf, (180, 180, 180), exit_button_rect, border_radius=15)

    display_surf.blit(
        exit_text,
        (
            exit_button_rect.centerx - exit_text.get_width() // 2,
            exit_button_rect.centery - exit_text.get_height() // 2
        )
    )

    # Check for user clicks on the buttons
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_again_button_rect.collidepoint(event.pos):
                main()
            elif exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()

def start_game(difficulty):
    """
    The main function of the program. It will handle the game loop and the events that occur during the game.

    The game loop will draw the tableau, stock, and foundation piles. It will also handle the dragging of cards from the tableau, stock, and foundation piles.

    There will be a difference in the number of cards drawn from the stock pile depending on the difficulty level. 
    In the easy level, only one card will be drawn, while in the hard level, three cards will be drawn.
    """
    global dragging, drag_card, drag_from, drag_offset, drag_pos, game_won

    if difficulty == "easy": # draw just one card at a time from stock
        talon_drag = 1

        def draw_talon():
            """
            This function will draw the talon pile with cards from the stock. We than add them to the talon_positions list.
            We use this list to be able to restore the stock after we have drawn all the cards from it.
            """
            global talon_positions
            talon_positions = []
            x = TALON_WIDTH_POS
            y = TALON_HEIGHT_POS
            card = talon[0]
            display_surf.blit(card_images[(card[0], card[1])], (x, y))
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            talon_positions.append(card_rect)

        def draw_from_stock():
            """
            This function is used to draw a card from the stock pile and add it to the talon pile.
            """
            global talon, stock
            if 50 <= mouse_pos[0] <= 121 and 50 <= mouse_pos[1] <= 146 and len(stock) > 1:
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
            """
            This function will draw the talon pile with 3 cards from the stock at each draw, because we are playing on the hard level.
            It will display the cards with a small overlap between them, so the player can see all three cards drawn.
            """
            global talon_positions
            talon_positions = []
            x = TALON_WIDTH_POS
            y = TALON_HEIGHT_POS
            overlap = 20
            for i, card in enumerate(talon):
                card_x = x + (i * overlap)
                display_surf.blit(card_images[(card[0], card[1])], (card_x, y))
                card_rect = pygame.Rect(card_x, y, CARD_WIDTH, CARD_HEIGHT)
                talon_positions.append(card_rect)

        def draw_from_stock():
            """
            This function is used to draw 3 cards from the stock pile and add it to the talon pile.
            """
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

    # This is the game main loop
    while True:
        if win_game():
            draw_win_screen()
        else:
            display_surf.fill(BG_COLOR)
            check_new_game_button_click()
            draw_new_game_button()
            draw_tableau()
            draw_stock()
            draw_foundations()
            if talon:
                draw_talon()
            if dragging:
                y_offset = 0
                for card in drag_card:
                    display_surf.blit(
                        card_images[(card[0], card[1])],
                        (drag_pos[0], drag_pos[1] + y_offset),
                    )
                    y_offset += 30

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    draw_from_stock() # draw from the stock

                    # drag from talon
                    if talon:
                        for index, rect in enumerate(reversed(talon_positions)):
                            if rect.collidepoint(mouse_pos):
                                dragging = True
                                drag_card = [talon.pop(index - 1)]
                                drag_from = ("talon", index)
                                drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                                drag_pos = (rect.x, rect.y)
                                talon_drag -= 1
                                break

                    # drag from foundations
                    for key in foundations:
                        if foundations[key]:
                            rect = pygame.Rect(
                                FOUNDATIONS_WIDTH_POS
                                + (list(foundations.keys()).index(key)) * 100,
                                FOUNDATIONS_HEIGHT_POS,
                                CARD_WIDTH,
                                CARD_HEIGHT,
                            )
                            if rect.collidepoint(mouse_pos):
                                dragging = True
                                drag_card = [foundations[key].pop()]
                                drag_from = ("foundations", key)
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
                                    drag_from = ("tableau", (key, index))
                                    drag_offset = (
                                        mouse_pos[0] - rect.x,
                                        mouse_pos[1] - rect.y,
                                    )
                                    drag_pos = (rect.x, rect.y)
                                    tableau[key] = tableau[key][:index]
                                    break
                        if dragging:
                            break

                if event.type == MOUSEMOTION and dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    drag_pos = (
                        mouse_pos[0] - drag_offset[0],
                        mouse_pos[1] - drag_offset[1],
                    )

                if event.type == MOUSEBUTTONUP and dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    placed = False

                    # try to place on tableau
                    if not placed:
                        for key in tableau:
                            pile_x = TABLEAU_WIDTH_POS + (int(key) - 1) * 100
                            last_card_y = (
                                TABLEAU_HEIGHT_POS + (len(tableau[key]) - 1) * 20
                            )
                            # extend with 20px to be sure the hitbox is matched  
                            last_card_rect = pygame.Rect(
                                pile_x + 20,
                                last_card_y + 20,
                                CARD_WIDTH + 20,
                                CARD_HEIGHT + 20,
                            )
                            if last_card_rect.collidepoint(mouse_pos):
                                if can_place_on_tableau(tableau[key], drag_card[0]):
                                    tableau[key].extend(drag_card)
                                    placed = True
                                    if "talon" in drag_from:
                                        cards_to_remove.append(drag_card)
                                    if "tableau" in drag_from:
                                        if tableau[drag_from[1][0]]:
                                            tableau[drag_from[1][0]][-1] = (
                                                tableau[drag_from[1][0]][-1][0],
                                                tableau[drag_from[1][0]][-1][1],
                                                True,
                                            )
                                        else:
                                            tableau[drag_from[1][0]] = []
                                break

                    # try to place on foundation
                    if not placed:
                        if len(drag_card) == 1:
                            suits = ["hearts", "diamonds", "clubs", "spades"]
                            for i, suit in enumerate(suits):
                                x = FOUNDATIONS_WIDTH_POS + i * 100
                                y = FOUNDATIONS_HEIGHT_POS
                                found_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                                if found_rect.collidepoint(mouse_pos):
                                    if can_place_on_foundation(
                                        foundations[suit], drag_card[0]
                                    ):
                                        foundations[suit].append(drag_card[0])
                                        placed = True
                                        if "talon" in drag_from:
                                            cards_to_remove.append(drag_card)
                                        if "tableau" in drag_from:
                                            if tableau[drag_from[1][0]]:
                                                tableau[drag_from[1][0]][-1] = (
                                                    tableau[drag_from[1][0]][-1][0],
                                                    tableau[drag_from[1][0]][-1][1],
                                                    True,
                                                )
                                            else:
                                                tableau[drag_from[1][0]] = []

                    # if the card was not placed, return it to its original position
                    if not placed:
                        if drag_from[0] == "talon":
                            talon.append(drag_card[0])
                            talon_drag += 1
                        elif drag_from[0] == "tableau":
                            tableau[drag_from[1][0]].extend(drag_card)
                        elif drag_from[0] == "foundations":
                            foundations[drag_from[1]].append(drag_card[0])

                    dragging = False
                    drag_card = []
                    drag_from = None

            draw_timer()
        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    """
    This is the main function of the program. It will start the game by displaying the intro screen with the buttons for choosing the difficulty level.
    """
    global start_time
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
                    start_time = pygame.time.get_ticks()
                    start_game("easy")
                elif hard_button_rect.collidepoint(mouse_pos):
                    intro = False
                    start_time = pygame.time.get_ticks()
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
