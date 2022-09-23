# coding:utf-8
import hashlib
import string
import sys
import urllib.request
import urllib.response
import urllib.error
from utils import *


class Cracker:
    @staticmethod
    def crack_dict(md5, file, order, done_queue):
        """
        Casse un HASH MD5 (md5) via une liste de mots-clés (file)
        :param done_queue:
        :param order:
        :param md5: Hash MD5 à casser
        :param file: Fichier de mots-clés à utiliser
        :return:
        """

        try:
            trouve = False
            ofile = open(file, "r")
            if Order.ASCEND == order:
                contenu = reversed(list(ofile.readlines()))
            else:
                contenu = ofile.readlines()
            for mot in contenu:
                mot = mot.strip("\n")
                hashmd5 = hashlib.md5(mot.encode("utf8")).hexdigest()
                if hashmd5 == md5:
                    trouve = True
                    print(Couleur.VERT + "[+] MOT DE PASSE TROUVÉ : " + mot + " (" + hashmd5 + ")" + Couleur.FIN)
                    done_queue.put("TROUVE")
                    break
            if not trouve:
                print(Couleur.ROUGE + "[-] MOT DE PASSE NON TROUVÉ :(" + Couleur.FIN)
                done_queue.put("NON TROUVE")
            ofile.close()
        except FileNotFoundError:
            print(Couleur.ROUGE + "[-] ERREUR : nom de dossier ou fichier introuvable !" + Couleur.FIN)
            sys.exit(1)
        except Exception as err:
            print(Couleur.ROUGE + "[-] ERREUR : " + str(err) + Couleur.FIN)
            sys.exit(2)

    @staticmethod
    def crack_incr(md5, length, _currpass=[]):
        """
        Casse un HASH MD5 via une méthode incrémentale pour un mdp de longueur length
        :param md5: Le hash md5 à casser
        :param length: La longueur du mot de passe à trouver
        :param _currpass: liste temporaire automatiquement utilisée via récursion contenant l'essai de mdp actuel
        :return:
        """

        lettres = string.printable

        if length >= 1:
            if len(_currpass) == 0:
                _currpass = ['a' for _ in range(length)]
                Cracker.crack_incr(md5, length, _currpass)
            else:
                for c in lettres:
                    _currpass[length - 1] = c
                    currhash = hashlib.md5("".join(_currpass).encode("utf8")).hexdigest()
                    print("[*] TEST DE : " + "".join(_currpass) + " (" + currhash + ")")
                    if currhash == md5:
                        print(Couleur.VERT + "[+] MOT DE PASSE TROUVÉ : " + "".join(_currpass) + Couleur.FIN)
                        sys.exit(0)
                    else:
                        Cracker.crack_incr(md5, length - 1, _currpass)
        else:
            return

    @staticmethod
    def crack_en_ligne(md5):
        """
        Cherche un HASH MD5 via google.fr
        :param:md5 hash md5 à utiliser pour la recherche en ligne
        :return:
        """

        try:
            agent_utilisateur = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
            headers = {'User-Agent': agent_utilisateur}
            url = "https://www.google.fr/search?hl=fr&q=" + md5
            requete = urllib.request.Request(url, None, headers)
            reponse = urllib.request.urlopen(requete)
        except urllib.error.HTTPError as e:
            print(Couleur.ROUGE + "[-] Erreur HTTP : " + e.code + Couleur.FIN)
        except urllib.error.URLError as e:
            print(Couleur.ROUGE + "[-] Erreur d'URL : " + e.reason + Couleur.FIN)

        if "Aucun document" in reponse.read().decode("utf8"):
            print(Couleur.ROUGE + "[-] HASH NON TROUVE VIA GOOGLE" + Couleur.FIN)
        else:
            print(Couleur.VERT + "[+] MOT DE PASSE TROUVE VIA GOOGLE : " + url + Couleur.FIN)

    @staticmethod
    def crack_smart(md5, pattern, _index=0):
        """
        :param md5:
        :param pattern:
        :param _index:
        :return:
        """
        MAJ = string.ascii_uppercase
        CHIFFRES = string.digits
        MIN = string.ascii_lowercase

        if _index < len(pattern):
            if pattern[_index] in MAJ + CHIFFRES + MIN:
                Cracker.crack_smart(md5, pattern, _index + 1)
            if "^" == pattern[_index]:
                for c in MAJ:
                    p = pattern.replace("^", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Couleur.VERT + "[+] MOT DE PASSE TROUVE : " + p + Couleur.FIN)
                        sys.exit(0)
                    print("[*] TEST DE : " + p + " (" + currhash + ")")
                    Cracker.crack_smart(md5, p, _index + 1)

            if "*" == pattern[_index]:
                for c in MIN:
                    p = pattern.replace("*", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Couleur.VERT + "[+] MOT DE PASSE TROUVE : " + p + Couleur.FIN)
                        sys.exit(0)
                    print("[*] TEST DE : " + p + " (" + currhash + ")")
                    Cracker.crack_smart(md5, p, _index + 1)

            if "²" == pattern[_index]:
                for c in CHIFFRES:
                    p = pattern.replace("²", c, 1)
                    currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if currhash == md5:
                        print(Couleur.VERT + "[+] MOT DE PASSE TROUVE : " + p + Couleur.FIN)
                        sys.exit(0)
                    print("[*] TEST DE : " + p + " (" + currhash + ")")
                    Cracker.crack_smart(md5, p, _index + 1)
        else:
            return

    @staticmethod
    def work(work_queue, done_queue, md5, file, order):
        """

        :param work_queue:
        :param done_queue:
        :param md5:
        :param file:
        :param order:
        :return:
        """
        o = work_queue.get()
        o.crack_dict(md5, file, order, done_queue)
