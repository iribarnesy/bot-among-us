from enum import Enum

class SentencesForRoom(Enum):
    A = "I entered {}".format
    B = "I walked on the floor of {}".format
    C = "I walked around {} with my heart open to the unknown".format
    D = "I was at {}".format
    E = "The life of me I was at {}".format
    F = "I don't remember, I think I was at {}".format

class SentencesForPlayersAppeared(Enum):
    A = "I saw {}".format
    B = "I crossed {}".format 
    C = "{} was with me".format
    D = "{} was there".format
class SentencesForPlayersDisappeared(Enum):
    A = "I saw more {}".format
    B = "{} disappeared".format
    C = "{} left like a ninja".format

class SentencesForPlayersKilled(Enum):
    A = "I saw a dead body, it was {}".format
    B = "{}'s blood spurted everywhere".format
    C = "{} is no more".format
    D = "I saw {} beheaded".format
    E = "I passed {} without a head".format
    F = "I passed {}'s spine".format

class SentencesForTaskDone(Enum):
    A = "I finished the task {}".format
    B = "{} finished".format
    C = "{} is finished".format


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

class TranslationToEnglish(Enum):
    crewmate = "crewmate"
    vent = "vent"
    RED_PLAYER = "Red"
    BLUE_PLAYER = "Blue"
    GREEN_PLAYER = "Green"
    YELLOW_PLAYER = "Yellow"
    ORANGE_PLAYER = "Orange"
    PINK_PLAYER = "Pink"
    PURPLE_PLAYER = "Purple"
    WHITE_PLAYER = "White"
    BLACK_PLAYER = "Black"
    BROWN_PLAYER = "Brown"
    CYAN_PLAYER = "Cyan"
    LIME_PLAYER = "Lime"
    ALONE = "Nobody"
    
class TranslationToGameLanguage(Enum):
    équipier = "crewmate"
    équipiers = "crewmates"
    trappe = "vinte"
    trappes = "vintes"
