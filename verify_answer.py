def normalize_string(s):

    s = s.lower()
    # Supprimer les espaces au début et à la fin
    s = s.strip()

    s = s.replace('é', 'e')
    s = s.replace('ï', 'i')

    s = s.replace('.', '')
    s = s.replace('"', '')
    s = s.replace("l'", '')

    # s.replace('î', 'i')
    # Supprimer les espaces doubles ou plus
    s = ' '.join(s.split())
    # on va gérér les mots entre parenthèse: on les enlève
    pos1 = s.find("(")
    if pos1 != -1:
        first = s[0:pos1]

        pos2 = s.find(")")
        if pos2 == -1:
            pos2 = len(s)
        second = s[pos2+1::] if pos2 + 1 < len(s) else ''

        s = first + second

    # Liste des articles à exclure en françaisf
    articles = ['un', 'une', 'le', 'la', 'les',"l'", ',', "du", "de", 'en', 'au', 'à','aux']
    # Séparer les mots de la chaîne
    words = s.split()
    # Exclure les articles de la liste des mots

    tokens = [word for word in words if word not in articles]

    if len(tokens) == 0:
        return words
    return tokens


def judge_if_true(user_answer, answer):
    user_words = normalize_string(user_answer)
    answer_words = normalize_string(answer)

    s = 0
    for word in user_words:
        if word in answer_words:
            s += 1

    return s/len(answer_words)
