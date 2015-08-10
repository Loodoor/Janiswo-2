# -*-coding: utf8-*

import pickle
import os
import sys
import random
import re
import time
import glob
import subprocess
from colorama import init, Fore
import webbrowser as wb
import serveur_http_local as srvweb
import platform as p
import socket
import web_page
import speech_recognition as spr
import speech_reco
import enasu
from threading import Thread
import remind


def is_path(path):
    if os.path.exists(path) and not os.path.isfile(path):
        return True
    return False


class Speaker():
    def __init__(self, os_logo, name='syntaxe_als'):
        self.commands = {}
        self.project_name = "Janiswö"
        self.recognizer = speech_reco.SpeechRecognition()
        self.os_logo = os_logo
        self.version = '0.0.1-a'
        self.location = os.path.dirname(os.path.abspath(__file__)) + "\\"
        self.builtins_methode = [
            'lst',
            'dir',
            'wsearch',
            'wsimage',
            'curdir',
            'whoami',
            'remind',
            'lst_reminds',
            'restart',
            'clear_cmd',
            'cls',
            'dcode',
            'pwds',
            'new_pwd',
            'backup',
            'sharef',
            'speech',
            'chcl',
            'chbr',
            'load',
            'curbck',
            'avaible_bck',
            'rw',
            'sudo',
            'unsudo',
            'myweb',
            'modules'
        ]
        self.passwords = {}
        self.reminders = []
        self.continuer = 1
        self.i = "In[0]: "
        self.o = "Out[1]: "
        self.s = "Save[2]: "
        self.extension = '.stx'
        self.name = name
        self.e_cl = Fore.RED
        self.i_cl = Fore.GREEN
        self.o_cl = Fore.CYAN
        self.s_cl = Fore.BLUE
        self.a_cl = Fore.YELLOW
        self.default_cl = Fore.WHITE
        self.cl(self.default_cl)
        self.admin = False
        self.current_backup = "std"
        self.basic_search = "http://google.fr/search?gws_rd=ssl&q="
        self.image_search = "http://google.fr/search?tbm=isch&gws_rd=ssl&q="
        self.speech_ = False
        self.recognizer = speech_reco.SpeechRecognition(name=self.project_name)
        self.thk = speech_reco.Think()
        self.welcome_home()

    @staticmethod
    def cls():
        os.system('cls')

    @staticmethod
    def cl(nom):
        # on évite print à cause du '\n' inséré automatiquement
        # sys.stdout.write(self.colours[nom])
        init()
        print('%s' % nom, end='')

    @staticmethod
    def myweb():
        web_page.main()

    def chbr(self):
        self.cl(self.i_cl)
        choix = input(self.i + "Quel prompt voulez vous modifier [input|output|save] ? ")
        if choix in ["input", "output", "save"]:
            new_br = input(self.i + "Nouvelle valeur pour le prompteur " + choix + " : ")
            if choix == "input":
                self.i = new_br
            if choix == "output":
                self.o = new_br
            if choix == "save":
                self.s = new_br
        else:
            self.cl(self.e_cl)
            print(self.o + "Erreur : le prompt demandé n'est pas valide")
        self.cl(self.default_cl)

    def chcl(self):
        self.cl(self.i_cl)
        cl_modif = input(self.i + "Quelle couleur voulez vous modifier\n[input|output|error|save|add] ? ")
        self.cl(self.o_cl)
        print(self.o + "Couleurs disponnibles :\nRED, GREEN, BLUE, CYAN, YELLOW, MAGENTA, WHITE, BLACK")
        if cl_modif in ['input', 'output', 'error', 'save', 'add']:
            new_cl = input(self.i + "Nouvelle couleur pour " + cl_modif + " : ")
            if new_cl in ["RED", "GREEN", "BLUE", "CYAN", "YELLOW", "MAGENTA", "WHITE", "BLACK"]:
                if cl_modif == 'input':
                    self.i_cl = getattr(Fore, new_cl)
                if cl_modif == 'output':
                    self.o_cl = getattr(Fore, new_cl)
                if cl_modif == 'error':
                    self.e_cl = getattr(Fore, new_cl)
                if cl_modif == "save":
                    self.s_cl = getattr(Fore, new_cl)
                if cl_modif == "add":
                    self.a_cl = getattr(Fore, new_cl)
            else:
                self.cl(self.e_cl)
                print(self.o + "Erreur : la couleur demandée n'est pas valide")
        else:
            self.cl(self.e_cl)
            print(self.o + "Erreur : l'action demandée n'est pas valide")
        self.cl(self.default_cl)

    def curdir(self):
        self.cl(self.o_cl)
        print(self.o + self.location + " est le répertoire courant.")
        if self.admin:
            self.cl(self.i_cl)
            choix = input(self.i + "Nouveau répertoire (chemin en absolu) : ")
            if is_path(choix):
                self.location = choix
                self.cl(self.o_cl)
                print(self.o + "Le répertoire courant est désormais : " + self.location)
            else:
                self.cl(self.e_cl)
                print(self.o + "Erreur : le répertoire demandé n'existe pas !")
        self.cl(self.default_cl)

    def pwds(self):
        self.cl(self.o_cl)
        print(self.o + "Liste des mots de passe enregistrés :")
        if not self.admin:
            for k, v in self.passwords.items():
                print(self.o + k + " : " + v + ", base : " + v[-1])
        else:
            if input(self.i + "Voulez vous afficher les mots de passe en clair [o|n] ? ").lower() == 'o':
                pass
        self.cl(self.default_cl)

    def new_pwd(self):
        self.cl(self.i_cl)
        cat = input(self.i + "Catégorie du mot de passe : ")
        pwd = enasu.get_and_encrypt(self.i)
        self.passwords[cat] = pwd
        self.cl(self.o_cl)
        print(self.o + "Mot de passe pour '" + cat + "' enregistré !")
        self.cl(self.default_cl)

    def remind(self):
        self.cl(self.i_cl)
        rap = input(self.i + "Rappel > ")
        date = input(self.i + "Quand [jj[/mm[/aaaa]]] || [hh[:mm[:ss]]] ? > ")
        date = re.sub(r' */* ', ' ', date)
        date = re.sub(r' *:* ', ' ', date)
        date = date.split(' ')

        self.reminders.append([rap, date])
        self.cl(self.o_cl)
        self.cl(self.default_cl)

    def lst_reminds(self):
        self.cl(self.o_cl)
        for i in self.reminders:
            print(self.o + ' '.join(i[1]) + ' : ' + i[0])
        self.cl(self.default_cl)

    def check_reminds(self):
        #à mettre dans un thread !
        possibilities = [
            '%d %m %Y',
            '%d %m',
            '%d',
            '%H %M %S',
            '%H %M',
            '%H'
        ]
        for i in self.reminders:
            date = ' '.join(i[1])
            for j in possibilities:
                if date == time.strftime(j):
                    remind.main(self.reminders[0], date, True)

    def scan(self, choix):
        self.cl(self.o_cl)
        print(self.o + "Liste des fichiers|dossiers du répertoire :")
        for i in os.listdir(self.location + choix):
            print("- " + i)

    def dir(self):
        self.cl(self.i_cl)
        choix = input(self.i + "Nom du répertoire à scanner : ")
        if is_path(self.location + choix):
            self.scan(choix)
        elif is_path(choix):
            self.scan(choix)
        else:
            self.cl(self.e_cl)
            print(self.o + "Erreur : le répertoire demandé n'existe pas !")
        self.cl(self.default_cl)

    def modules(self):
        self.cl(self.o_cl)
        modulenames = set(sys.modules) & set(globals())
        for i in modulenames:
            print(self.o + str(i) + " a été initialisé")
        self.cl(self.default_cl)

    def sudo(self):
        self.cl(self.o_cl)
        if not self.admin:
            self.admin = True
            print(self.o + "Mode Administrateur activé")
        else:
            print(self.o + "Le mode Administrateur est déjà actif")
        self.cl(self.default_cl)

    def unsudo(self):
        self.cl(self.o_cl)
        if self.admin:
            self.admin = False
            print(self.o + "Mode Administrateur désactivé")
        else:
            print(self.o + "Le mode Adminstrateur est déjà inactif")
        self.cl(self.default_cl)

    def curbck(self):
        self.cl(self.o_cl)
        print(self.o + "Le backup actuellement utilisé est '" + self.current_backup + "'")

    def add_command(self, command, action):
        self.commands[command] = action
        self.cl(self.a_cl)
        print(self.s + command + ':' + action)
        self.cl(self.default_cl)

    def whoami(self):
        self.cl(self.o_cl)
        result = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE).stdout.read()
        adresse_mac = re.search('([0-9A-F]{2}-?){6}', str(result)).group()
        adresse_mac = adresse_mac.split('-')
        adresse_mac = ':'.join(adresse_mac)
        systeme = p.system()
        jeu, format_fichier = p.architecture()
        distribution = p.version()
        hote = socket.gethostbyname(socket.gethostname())
        to_test = [
            ["Nom d'utilisateur", os.getenv('USERNAME')],
            ["Système opérant", systeme],
            ["Version", distribution],
            ["Adresse IP locale", hote],
            ["Adresse MAC", adresse_mac],
            ["Type de processeur", jeu],
            ["Format des fichiers", format_fichier]
        ]
        for k in to_test:
            print(self.o + k[0] + " : " + k[1])
        self.cl(self.default_cl)

    def welcome_home(self):
        self.cl(self.s_cl)
        print(self.os_logo)
        self.cl(self.default_cl)
        self.cl(self.default_cl)
        print(self.project_name + " " + self.version + "\n")
        self.load_stx(self.name)

    def clear_cmd(self):
        self.cl(self.i_cl)
        choix = input(self.i + "Etes vous sûr de vouloir effacer toutes les commandes [o|n] ? ").lower()
        self.cl(self.default_cl)
        if self.admin:
            if choix == 'o':
                self.cl(self.o_cl)
                print(self.o + "Suppression des commandes déjà enregistrées ...")
                self.cl(self.default_cl)
                self.commands = {}
        else:
            self.cl(self.e_cl)
            print(self.o + "Erreur ! Vous n'êtes pas Administrateur")
            self.cl(self.default_cl)

    def avaible_bck(self):
        self.cl(self.o_cl)
        print(self.o + "Liste des backups disponnibles :")
        for path in glob.glob(self.location + "BACKUPS/*" + self.extension):
            print("- " + path[len(self.location) + len("BAKCUPS/"):-4])
        self.cl(self.default_cl)

    def sharef(self):
        self.cl(self.a_cl)
        srvweb.main()
        self.cl(self.default_cl)

    def restart(self):
        self.save_stx(name=self.name)
        print("\n" + "-" * 80)
        self.continuer = 0
        self.cls()
        subprocess.Popen(['py', '-3.4', 'janiswo.py'])

    def backup(self):
        self.cl(self.i_cl)
        name_bkp = input(self.i + "Nom de la sauvegarde : ").lower()
        self.cl(self.default_cl)
        self.save_stx(name=name_bkp)
        self.cl(self.o_cl)
        print(self.o + "'" + name_bkp + "' a été sauvegardé !")
        self.cl(self.default_cl)

    def load(self, arg=''):
        self.save_stx(name=self.name)
        self.cl(self.i_cl)
        self.current_backup = arg
        if arg == '':
            new_stx = input(self.i + "Nom du backup à charger : ").lower()
            self.cl(self.default_cl)
            if os.path.exists("BACKUPS/" + new_stx + self.extension):
                self.load_stx(new_stx)
                self.cl(self.o_cl)
                print(self.o + new_stx + " a été chargé")
                self.cl(self.default_cl)
            else:
                self.cl(self.e_cl)
                print(self.o + "Erreur: impossible d'initialiser " + new_stx)
                self.cl(self.default_cl)
            self.current_backup = new_stx
        else:
            if os.path.exists("BACKUPS/" + arg + self.extension):
                self.load_stx(arg)
                self.cl(self.o_cl)
                print(self.o + arg + " a été chargé")
                self.cl(self.default_cl)
            else:
                self.cl(self.e_cl)
                print(self.o + "Erreur: impossible d'initialiser " + arg)
                self.cl(self.default_cl)

    def wsearch(self, arg=''):
        self.cl(self.i_cl)
        if arg == '':
            search = input(self.i + "Recherche : ")
            self.cl(self.default_cl)
        else:
            search = arg
        if not re.match(r'[http|https]?[://]?[www\.]?.+\..{2,4}/?.*', search):
            #on fait une recherche
            wb.open(self.basic_search + search)
        else:
            #on veut aller sur un site web
            wb.open(search)
        self.cl(self.default_cl)

    def wsimage(self, arg=''):
        self.cl(self.i_cl)
        if arg == '':
            search = input(self.i + "Recherche : ")
            self.cl(self.default_cl)
        else:
            search = arg
        wb.open(self.image_search + search)
        self.cl(self.default_cl)

    def dcode(self, arg=''):
        self.cl(self.i_cl)
        if arg == '':
            arg = input(self.i + "Nom de la commande : ")
        self.cl(self.o_cl)
        if arg in self.commands.keys():
            print(self.o + "Code de la commande '" + arg + "' :")
            print(str(self.commands[arg]))
        elif arg in self.builtins_methode:
            print(self.o + "Code de la commande '" + arg + "' :")
            print(str(exec("self." + arg + "()")))
        else:
            print(self.o + "La commande n'existe pas")
        self.cl(self.default_cl)

    def speech(self, arg=''):
        self.cl(self.i_cl)
        if arg == '':
            arg = input(self.i + "[On|Off] : ")
        self.cl(self.o_cl)
        if arg.lower() == 'on':
            self.speech_ = True
            print(self.o + "Le TTS et la speech recognition sont désormais actif")
        elif arg.lower() == 'off':
            self.speech_ = False
            print(self.o + "Le TTS et la speech recognition sont désormais inactif")
        self.cl(self.default_cl)

    def try_recognizing(self, texte):
        possibility = []
        for j in self.builtins_methode:
            if len(j) - 1 <= len(texte) <= len(j) + 1:
                temp1 = sorted(j)
                temp2 = sorted(texte)
                ok = False
                if len(temp1) > len(temp2):
                    for i in temp2:
                        if i in temp1:
                            ok = True
                        else:
                            ok = False
                            break
                elif len(temp2) > len(temp1):
                    for k in temp1:
                        if k in temp2:
                            ok = True
                        else:
                            ok = False
                            break
                if ok:
                    possibility.append(j)
        if possibility:
            self.cl(self.i_cl)
            if input(self.i + "Vous vouliez probablement exécuter " + possibility[0] + " [o|n] ? ").lower() == 'o':
                self.cl(self.default_cl)
                return possibility[0]
            self.cl(self.default_cl)
        return ''

    def lst(self):
        self.cl(self.o_cl)
        print(self.o + "Liste des commandes :")
        if self.commands.keys():
            print(self.s_cl + "Commandes utilisateur :" + self.o_cl)
            for k in self.commands.keys():
                print("- " + k)
        print(self.s_cl + "Commandes builts in :" + self.o_cl)
        for l in self.builtins_methode:
            print("- " + l)
        self.cl(self.default_cl)

    def rw(self, arg=''):
        self.cl(self.i_cl)
        if arg == '':
            arg = input(self.i + "Nom de la commande à réécrire : ")
        if arg in self.commands.keys():
            self.cl(self.i_cl)
            buffer = ""
            while 1:
                code = input('... ')
                if code != '':
                    buffer += "\n" + code
                else:
                    break
            self.commands[arg] = buffer
        else:
            self.cl(self.o_cl)
            print(self.o + "Cette commande n'existe pas !")
        self.cl(self.o_cl)
        print(self.o + "Le code de la commande '" + arg + "' a bien été modifié")
        self.cl(self.default_cl)

    def new(self, input_usr):
        if 'aka' not in input_usr:
            input_usr = re.sub(r' +', '-', input_usr)
            self.cl(self.o_cl)
            print(self.o + 'Commande ' + input_usr + ' non reconnue.')
            self.cl(self.default_cl)
        else:
            self.cl(self.o_cl)
            print(self.o + 'Commande multiple non reconnue.')
            self.cl(self.default_cl)
        self.cl(self.i_cl)
        if input(self.i + 'Souhaitez-vous l\'ajouter [o|n] ? ') == 'o':
            self.cl(self.default_cl)
            if 'aka' in input_usr:
                input_usr = re.sub(r' ?', '', input_usr).split('aka')
            self.cl(self.i_cl)
            prompt = input(self.i + 'Action à exécuter : ')
            input_spt = ' '
            if prompt[:3] == 'aka' and prompt[4:] in self.commands.keys():
                command_ = prompt[4:]
                prompt = self.commands[command_]
                input_spt = ''
            while input_spt != '':
                self.cl(self.i_cl)
                input_spt = input('... ')
                self.cl(self.default_cl)
                prompt += "\n"
                prompt += input_spt
            if isinstance(input_usr, list):
                for i in input_usr:
                    self.add_command(i, prompt)
            else:
                self.add_command(input_usr, prompt)
        self.cl(self.default_cl)

    def launch(self, arg):
        if arg in self.commands.keys():
            exec(self.commands[arg])
        elif arg in self.builtins_methode:
            exec("self." + arg + "()")

    def launch_pls(self, args):
        lst = args.split(' ')
        for i in range(len(lst)):
            self.launch(lst[i])

    def is_args_lst(self, texte):
        phr = texte.split(' ')
        for i in range(len(phr)):
            if phr[i] in self.builtins_methode or phr[i] in self.commands.keys():
                pass
            else:
                return False
        return True

    def start(self):
        #de manière à checker asynchronement les reminders
        Thread(target=self.check_reminds).start()
        while self.continuer:
            self.cl(self.i_cl)
            if self.speech_:
                print(self.i, end='')
                input_usr = self.recognizer.recognize()
                print(input_usr)
            else:
                input_usr = input(self.i)
            self.cl(self.default_cl)
            if input_usr == 'exit' or input_usr == 'quit':
                #on doit s'en aller #commantaireInutile
                self.save_stx(self.name)
                break
            #Zone des commandes à argument(s) unique ou multiples
            elif input_usr[:4] == 'load' and len(input_usr.split(' ')) >= 2:
                #on charge un backup
                self.load(arg=input_usr.split(' ')[1])
            elif input_usr[:7] == 'wsearch' and len(input_usr.split(' ')) >= 2:
                #recherche sur google
                self.wsearch(arg=' '.join(input_usr.split(' ')[1:]))
            elif input_usr[:7] == 'wsimage' and len(input_usr.split(' ')) >= 2:
                #recherche par image
                self.wsimage(arg=' '.join(input_usr.split(' ')[1:]))
            elif input_usr[:5] == 'dcode' and len(input_usr.split(' ')) >= 2:
                #on veut voir le code d'une commande
                self.dcode(arg=input_usr.split(' ')[1])
            elif input_usr[:2] == 'rw' and len(input_usr.split(' ')) >= 2:
                #on veut changer le code d'une commande
                self.rw(arg=input_usr.split(' ')[1])
            elif input_usr[:6] == 'speech' and len(input_usr.split(' ')) >= 2:
                #on veut changer l'etat de speech
                self.speech(arg=input_usr.split(' ')[1])
            #-----------------------------------------------------
            elif input_usr[:2] == '::' or not input_usr or input_usr == '\n':
                #commentaire
                pass
            elif self.is_args_lst(input_usr):
                #si il y a plusieurs commandes
                self.launch_pls(input_usr)
            elif input_usr not in self.commands.keys() and input_usr not in self.builtins_methode:
                #si on ne reconnait pas la commande
                recognize = self.try_recognizing(input_usr)
                if not recognize and not self.speech_:
                    self.new(input_usr)
                else:
                    self.launch(recognize)
            else:
                #sinon on lance la commande, sans argument(s)
                self.launch(input_usr)

    def save_stx(self, name='syntaxe_als'):
        if name == 'syntaxe_als':
            with open(self.location + name + self.extension, 'wb') as save_stx:
                pickle.Pickler(save_stx).dump(self.commands)
        else:
            with open(self.location + "BACKUPS/" + name + self.extension, 'wb') as save_stx:
                pickle.Pickler(save_stx).dump(self.commands)
        with open(self.location + "reminders.pkl", "wb") as save_reminds:
            pickle.Pickler(save_reminds).dump(self.reminders)
        with open(self.location + "pwds.pkl", "wb") as save_pwds:
            pickle.Pickler(save_pwds).dump(self.passwords)

    def load_stx(self, name='syntaxe_als'):
        if name != 'syntaxe_als':
            with open(self.location + "BACKUPS/" + name + self.extension, "rb") as read_stx:
                self.commands = pickle.Unpickler(read_stx).load()
        else:
            if os.path.exists(self.location + name + self.extension):
                with open(self.location + name + self.extension, "rb") as read_stx:
                    self.commands = pickle.Unpickler(read_stx).load()
        if os.path.exists(self.location + "reminders.pkl"):
            with open(self.location + "reminders.pkl", "rb") as read_reminds:
                self.reminders = pickle.Unpickler(read_reminds).load()
        if os.path.exists(self.location + "pwds.pkl"):
            with open(self.location + "pwds.pkl", "rb") as read_pwds:
                self.passwords = pickle.Unpickler(read_pwds).load()