
import time
import curses
import os
from random import choice, sample


from window_functions import init_ui, update_ui, display_message, display_state, pause
from verify_answer import judge_if_true


# TODO mettre en boucle la pose du fichier d'erreurs
#      ne pas prendre en compte les mots en parenthèse dans anwser
#      revoir le calcul des stats en bas pour les fichirs d'erreur
#      0 ou 1 pour oui ou non
#      ne pas réafficher la bonne réponse quand l'utilisateur trouve les 100%


chemin = "Base de données"
paths = []
for fichier in os.listdir(chemin):
    paths.append(fichier)

# choisi = "Genius_22.txt"
choisi = choice(paths)  # if you  want you can directly put here the name of
# file that you want to use

path = "Base de données\\" + choisi

print("\n", path[16::], "\n")


def main(stdscr):

    temps_limite = 18
    number_questions_to_ask = 35

    with open(path, 'r', encoding='utf-8') as file:
        lines_ = file.readlines()
        lines = []
        where = 0
        for line in lines_:
            where += 1
            if line == '\n':
                continue
            contain = line.strip().split(';')
            if len(contain) == 2:
                lines.append(line)
            else:
                print("A la ligne ", where, "du fichier ", path[16::], "le formattage n'est pas respecté ou soit il manque la réponse" )

    file = open("Resign_to_learn.txt", 'w', encoding='utf-8')
    timer_window, question_window, answer_window, message_window, state_window = init_ui(stdscr)

    score, where, true_questions = 0, 0, 0
    number = min(number_questions_to_ask, len(lines))
    total_questions = number

    # shuffle(lines) finalement on ne fera pas de répétition d''éléments
    for line in sample(lines, number):
        where += 1
        contain = line.strip().split(';')

        question, answer = contain
        answer = answer.replace('.', '')
        start_time = time.time()
        user_answer = ''
        user_input = ''

        stdscr.nodelay(1)
        while time.time() - start_time < temps_limite:
            time_left = int(temps_limite - (time.time() - start_time))
            update_ui(stdscr, timer_window, question_window, answer_window,
                      question, time_left,
                      user_input)

            c = stdscr.getch()
            if c != -1:
                if c == ord('\n'):
                    user_answer = user_input
                    break
                elif c == ord('\b'):
                    user_input = user_input[:-1]
                else:
                    user_input += chr(c)

        stdscr.nodelay(0)

        if time.time() - start_time > temps_limite:
            dire = f"\t{answer}"
            display_message(message_window, dire, state='Temps écoulé', refusé=1)
            continue

        similarity = judge_if_true(user_answer, answer)

        if similarity > 0.5:
            extra = answer if similarity < 1 else ''

            display_message(message_window, 'Bonne réponse!', color=1, extra=extra)
            score += 1
            true_questions += 1
        else:
            if user_answer == '':
                state = ''
            else:
                state = 'FALSE'
            display_message(message_window,
                            f"\t{answer}", state=state, refusé=1)
            file.write(line)

        remaining = total_questions-where
        display_state(state_window, score, remaining, true_questions,
                      where)

    # question_window.addstr(0, 0, "Voulez-vous reprendre les questions que vous n'avez pas trouvées?")
    message_window.addstr(0, 0, f"Score final : {score}/{total_questions}", curses.color_pair(5))
    message_window.refresh()
    # question_window.refresh()
    pause(message_window)


curses.wrapper(main)

while True:
    print("\nEtes vous prêt à affronter vos erreurs,\n Entrez 1 pour oui et 0 si non ")
    c = input('\t: ').strip().lower()

    if c == "1" or c == "oui":
        path = "Resign_to_learn.txt"
        curses.wrapper(main)
    else:
        print("Merci pour l'utilisation, méditez sur vos nouvelles connaissances\n\n")
        break
    
