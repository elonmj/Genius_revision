

import time
import curses


# TO DO
# je dois m'arranger pour que s'il y a trois prénoms, on puisse en citer deux et avoir le point
# je dois également faire une visualisation du nombre de points accumulés pendant le questionnaire 
# et aussi du nombre de questions restantes
# je dois retourner dans un fichier txt toutes les questions ratées, il sera renouvelés à chaque exécution


def init_ui(stdscr):
    curses.curs_set(0)  # Désactiver le curseur

    # Obtenir les dimensions de la fenêtre principale
    max_y, max_x = stdscr.getmaxyx()

    max_y, max_x = max_y-2, max_x-8
    # Calculer la largeur de la fenêtre du minuteur
    timer_width = max_x
    # Créer une fenêtre pour le minuteur
    timer_window = stdscr.subwin(1, timer_width, 1, 4)

    # Calculer les dimensions de la fenêtre de la question
    question_height = 10
    question_width = max_x
    # Créer une fenêtre pour la question
    question_window = stdscr.subwin(question_height, question_width, 3, 4)

    # Calculer les dimensions de la fenêtre de réponse
    answer_width = max_x
    # Créer une fenêtre pour la réponse
    answer_window = stdscr.subwin(1, answer_width, 15, 4)

    # Calculer les dimensions de la fenêtre des messages
    message_width = max_x
    # Créer une fenêtre pour les messages
    message_window = stdscr.subwin(2, message_width, 17, 4)

    # fenêtre pour afficher le nombre de questions et le score actuel
    state_window = stdscr.subwin(4, max_x, 23, 4)
    # on va gérer la couleur aussi
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    return timer_window, question_window, answer_window, message_window, state_window


def update_ui(stdscr, timer_window, question_window, answer_window, question, time_left, user_input):
    # Effacer les fenêtres
    timer_window.clear()
    question_window.clear()
    answer_window.clear()

    # Afficher le minuteur
    timer_window.addstr(0, 0, f"\t{time_left}", curses.color_pair(3))

    timer_window.addstr(0, 11, "secondes")

    # Afficher la question
    question_window.addstr(0, 0, question, curses.color_pair(1))

    # Afficher la réponse de l'utilisateur
    answer_window.addstr(0, 0, "R:", curses.color_pair(4))
    answer_window.addstr(0, 2, f"\t{user_input}")

    # Rafraîchir toutes les fenêtres en une seule opération
    answer_window.refresh()
    question_window.refresh()
    timer_window.refresh()


def pause(stdscr):
    stdscr.timeout(-1)  # Désactiver le timeout

    while stdscr.getch() != ord('\n'):
        pass

    stdscr.timeout(400)  # Rétablir le timeout à 500 millisecondes


def display_message(message_window, message, state="FALSE", refusé=0, color=4, extra=''):

    if refusé and state != '':
        message_window.addstr(0, 0, state, curses.color_pair(2))
        message_window.refresh()

        start_time = time.time()
        while time.time() - start_time < 0.35:
            pass
        message_window.clear()
        message_window.refresh()

    max_x = message_window.getmaxyx()[1] - 8
    if len(message) > max_x or len(extra) > max_x:
        message = message + extra
        message_window.addstr(0, 0, message[0:max_x], curses.color_pair(color))
        message_window.addstr(1, 0, '\t' + message[max_x::], curses.color_pair(color))
    else:
        message_window.addstr(0, 0, message, curses.color_pair(color))
        if extra != '':
            message_window.addstr(0, len(message) + 4, extra, curses.color_pair(4))

    message_window.refresh()

    pause(message_window)

    message_window.clear()
    message_window.refresh()


def display_state(stdscr, score, remaining, true_questions, where):

    stdscr.clear()

    sms1 = "Your score is "+str(score)
    sms2 = "It remains "+str(remaining)+" questions"
    sms3 = f"you've right answered to {true_questions} on {where}"

    stdscr.addstr(1, 0, sms1, curses.color_pair(6))

    stdscr.addstr(2, 0, sms2)  # , curses.color_pair(6))

    stdscr.addstr(3, 0, sms3)  # , curses.color_pair(6))
    stdscr.refresh()
