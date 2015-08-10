"""
auteur : Folaefolc
date : 10/08/15
license : MIT
"""

#-*-coding: Utf-8-*-

from math import *
from getpass import getpass
import random


def my_pi(cont):
    dt = 1
    tot = 0
    s = 0
    verif = 1
    cont = 2 if cont <= 1 else cont

    for i in range(cont):
        while tot <= 1:
            s += 4 * sqrt(1-pow(tot, 2)) * dt
            tot += dt
        dt *= 0.1
        tot = 0
        if i != cont - 1:
            s = 0
        verif += 1
    return s


def algo(txt, base, taille):
    lst_pi = [i for i in str(my_pi(base)) if i != '.']
    code = 0
    arithm = '+-*/'
    cur = 0
    for i in txt:
        code = eval(str(code) + arithm[cur] + str(ord(i)))
        cur += 1
        cur %= len(arithm)
    tmp = str(code)
    tmp = [k for k in tmp]
    if len(tmp) < taille:
        to_add = taille - len(tmp)
        for j in range(to_add):
            tmp.append(lst_pi[j])
        tmp[-1] = str(base)
    return ''.join(tmp)


def get_and_encrypt(opt=''):
    mdp = getpass(prompt=opt + "Mot de passe : ")
    hash_ = algo(mdp, random.randint(2, 5), 32)
    return hash_


if __name__ == '__main__':
    to_encrypt = input("Texte > ")
    base = int(input("dt = ? > "))
    taille_std = 32

    code = algo(to_encrypt, base, taille_std)
    print(code)
    print("Taille du hash : " + str(len(code)))


#exemple de hash pour "hello world", avec dt = 1 :
#   9390.990990990991330451833220871
#exemple de hash pour "hello world", avec dt = 3 :
#   9390.990990990991316041703177903

#exemple de hash pour "bonjour", avec dt = 1 :
#   -2221.92452830188633304518332201
#exemple de hash pour "bonjour", avec dt = 3 :
#   -2221.92452830188633160417031773


#exemplde de hash pour "salut le monde", avec dt = 1 :
#   29.86680744997576733045183322081
#exemplde de hash pour "salut le monde", avec dt = 3 :
#   29.86680744997576731604170317793