from enum import Enum

class SentencesForRoom(Enum):
    A = "Je suis entré à {}".format
    B = "J'ai foulé le sol de {}".format
    C = "Je me baladais dans {} , le coeur ouvert à l'inconnu".format
    D = "J'étais à {}".format
    E = "La vie de moi j'étais à {}".format
    F = "Je me rappelle plus, je crois que j'étais à {}".format

class SentencesForPlayersAppeared(Enum):
    A = "J'ai vu {}".format
    B = "J'ai croisé {}".format 
    C = "{} était avec moi".format
    D = "{} était là".format
class SentencesForPlayersDisappeared(Enum):
    A = "Je voyais plus {}".format
    B = "{} a disparu".format
    C = "{} est parti comme un ninja".format

class SentencesForPlayersKilled(Enum):
    A = "J'ai vu un cadavre, c'était {}".format
    B = "Le sang de {} a giclé partout".format
    C = "{} n'est plus".format
    D = "J'ai vu {} décapité".format
    E = "J'ai croisé {} sans tête".format
    F = "J'ai croisé la colonne vertébrale de {}".format

class SentencesForTaskDone(Enum):
    A = "J'ai fini la tâche {}".format
    B = "{} terminé".format
    C = "{} est fini".format


class SentencesRandom(Enum):
    A = "Tu buzz tu tej"

class TranslationToFrench(Enum):
    crewmate = "équipier"
    vent = "trappe"
    RED_PLAYER = "Rouge"
    BLUE_PLAYER = "Bleu"
    GREEN_PLAYER = "Vert"
    YELLOW_PLAYER = "Jaune"
    ORANGE_PLAYER = "Orange"
    PINK_PLAYER = "Rose"
    PURPLE_PLAYER = "Violet"
    WHITE_PLAYER = "Blanc"
    BLACK_PLAYER = "Noir"
    BROWN_PLAYER = "Marron"
    CYAN_PLAYER = "Cyan"
    LIME_PLAYER = "Citron vert"
    ALONE = "personne"

class TranslationToGameLanguage(Enum):
    équipier = "crewmate"
    équipiers = "crewmates"
    trappe = "vinte"
    trappes = "vintes"
