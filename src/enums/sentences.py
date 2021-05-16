from enum import Enum

class SentencesForRoom(Enum):
    A = "Je suis entré à {}".format
    B = "J'ai foulé le sol de {}".format

class SentencesForPlayersAppeared(Enum):
    A = "J'ai vu {}".format

class SentencesForPlayersDisappeared(Enum):
    A = "Je voyais plus {}".format

class SentencesForPlayersKilled(Enum):
    A = "J'ai vu un cadavre, c'était {}".format
    B = "Le sang de {} a giclé partout".format

class SentencesForTaskDone(Enum):
    A = "J'ai fini la tâche {}".format

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
