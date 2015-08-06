# -*-coding: utf8-*

import analyser as als
import sys
import os
import subprocess
import traceback


os_logo = "       @@@   @@@@@@   @@@  @@@  @@@   @@@@@@   @@@  @@@  @@@   @@@@@@\n       @@@  @@@@@@@@  @@@@ @@@  @@@  @@@@@@@   @@@  @@@  @@@  @@@@@@@@\n       @@!  @@!  @@@  @@!@!@@@  @@!  !@@       @@!  @@!  @@!  @@!  @@@\n       !@!  !@!  @!@  !@!!@!@!  !@!  !@!       !@!  !@!  !@!  !@!  @!@\n       !!@  @!@!@!@!  @!@ !!@!  !!@  !!@@!!    @!!  !!@  @!@  @!@  !@!\n       !!!  !!!@!!!!  !@!  !!!  !!!   !!@!!!   !@!  !!!  !@!  !@!  !!!\n       !!:  !!:  !!!  !!:  !!!  !!:       !:!  !!:  !!:  !!:  !!:  !!!\n  !!:  :!:  :!:  !:!  :!:  !:!  :!:      !:!   :!:  :!:  :!:  :!:  !:!\n  ::: : ::  ::   :::   ::   ::   ::  :::: ::    :::: :: :::   ::::: ::\n   : :::     :   : :  ::    :   :    :: : :      :: :  : :     : :  :   "


def post_mortem(exc_type, exc_val, exc_tb):
    os.system('cls')
    #BSoD à la windows 9x
    os.system("color 9f")
    print(os_logo + "\n")
    message_err = ["Une erreur fatale est surevenue.", "", ""]
    for i in message_err:
        print("\t\t" + i)
    #on affiche l'exception histoire de savoir ce qu'on debug
    print("\n" + str(exc_type) + " :: " + str(exc_val) + "\n" * 2)
    print(traceback.format_exception(exc_type, exc_val, exc_tb)[-2])
    waiter = input("\n\nAppuyez sur Entrer pour relancer Janiswö ... ")
    if waiter == 'explain me':
        print("\n\t\t\t\tTraceback complet\n")
        print("".join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        input('... ')
    elif waiter == "repear":
        if 'C:/Python34/lib/socket.py'.lower() in traceback.format_exception(exc_type, exc_val, exc_tb)[-4].lower():
            #on a eu un problème avec le module socket de python,
            #on doit le réparer
            with open("c:/python34/lib/socket.py", "r+") as socket_file:
                tmp = socket_file.readlines()
                print("Ligne problématique : " + tmp[460])
                tmp[460][-7:] = ''
                print("Ligne réparée : " + tmp[460])
                for i in tmp:
                    socket_file.write(i + "\n")
    os.system('cls')
    subprocess.Popen(['py', '-3.4', 'janiswo.py'])

#on dit à python de lancer cette fonction quand il plante
sys.excepthook = post_mortem


def go():
    os.system("color 0f")
    #on démarre l'analyser
    analyse_stx = als.Speaker(os_logo)
    #on démarre le noyau
    analyse_stx.start()

if __name__ == '__main__':
    go()