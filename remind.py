#-*-coding: utf-8-*-


def main(texte, quand, date):
    texte = "\tMonsieur, vous m'avez demandé de vous rappeler :\n" + texte
    choix = "; le " + quand if date else "; à " + quand
    print(texte + choix)