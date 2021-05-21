import time
import numpy as np
import pandas as pd
import cv2
from PIL import ImageGrab, Image
import pytesseract
import math
from enum import Enum
from shapely.geometry import Polygon, Point
from ast import literal_eval
import random

import src.utils as utils
from src.enums.texts import TasksTexts
from src.enums.sentences import SentencesForRoom, SentencesForPlayersAppeared, SentencesForPlayersDisappeared, SentencesForPlayersKilled, SentencesForTaskDone
from src.enums.sentences import TranslationToEnglish, TranslationToGameLanguage


class Log:
    def __init__(self, room, time=time.time(), players=[], killed=[], task=""):
        self.room = room # Cafet
        self.time = time # t secode
        self.players = players if type(players) == list else literal_eval(players) # [yellow ...]
        self.killed = killed if type(killed) == list else literal_eval(killed) # [pink ...]
        self.task = task if type(task) == str else ''


    def __repr__(self):
        retour = "(LOG) " + str(self.time) + " - " + str(self.room)
        if self.task != "":
            retour = retour + " - Task done : " + self.task
        if len(self.players) > 0:
            retour = retour + " - Players {"
            for player in self.players:
                retour = retour + player + ", "
            retour = retour [0:len(retour)-2] + "}"
        if len(self.killed) > 0:
            retour = retour + " - Killed {"
            for kill in self.killed:
                retour = retour + kill + ", "
            retour = retour[0:len(retour)-2]+ "}"

        return retour

    def log_to_dataframe(self):
        d = {'room': [self.room], 'time': [self.time], 'players': [self.players], 'killed': [self.killed], 'task': [self.task]}
        df = pd.DataFrame(data=d)
        return df
    
    def equal(self, Log):
        if Log.room == self.room and len(Log.players) == len(self.players) and len(Log.killed) == len(self.killed) and Log.task == self.task:
            for player in self.players:
                if(player not in Log.players):
                    return False
            for kill in self.killed:
                if(kill not in Log.killed):
                    return False
            return True
        else:
            return False


    """ Creation of sentences
    """
    def room_changed(self, Log):
        return self.room != Log.room
    def players_appeared(self, Log):
        return [player for player in Log.players if player not in self.players]
    def players_killed(self, Log):
        return [body for body in Log.killed if body not in self.killed]
    def players_disappeared(self, Log):
        return Log.players_appeared(self)
    def a_task_is_done(self, Log):
        return Log.task != ''
        
    def differences_with(self, Log):
        differences = {}

        if self.room_changed(Log):
            differences['room'] = Log.room

        def add_players_difference(players, name):
            if len(players) > 0:
                differences[name] = players
        add_players_difference(self.players_appeared(Log), 'players_appeared')
        add_players_difference(self.players_killed(Log), 'players_killed')
        add_players_difference(self.players_disappeared(Log), 'players_disappeared')

        if self.a_task_is_done(Log):
            differences['task'] = Log.task
        return differences

    def sentence_for_room(self, room):
        strf = random.choice(list(SentencesForRoom)).value
        return strf(room)
    def sentence_for_players_appeared(self, players):
        strf = random.choice(list(SentencesForPlayersAppeared)).value
        return strf(utils.join_words(players))
    def sentence_for_players_disappeared(self, players):
        strf = random.choice(list(SentencesForPlayersDisappeared)).value
        return strf(utils.join_words(players))
    def sentence_for_players_killed(self, players):
        strf = random.choice(list(SentencesForPlayersKilled)).value
        return strf(utils.join_words(players))
    def sentence_for_task_done(self, task):
        strf = random.choice(list(SentencesForTaskDone)).value
        return strf(task)

    def sentence(self, log):
        differences = self.differences_with(log)
        differences_to_sentence = {
            'room': self.sentence_for_room,
            'players_appeared': self.sentence_for_players_appeared,
            'players_killed': self.sentence_for_players_killed,
            'players_disappeared': self.sentence_for_players_disappeared,
            'task': self.sentence_for_task_done
        }
        sentence = [differences_to_sentence[key](value) for key, value in differences.items()]
        sentence = ". ".join(sentence)
        sentence_translated = Log.translate_sentence_to_english(sentence)
        return sentence_translated

    @staticmethod
    def translate_sentence_to_english(sentence):
        return utils.translate_from_enum(sentence, TranslationToEnglish)
    @staticmethod
    def translate_sentence_to_game_language(sentence):
        return utils.translate_from_enum(sentence, TranslationToGameLanguage)



    """ Static methods to work with dataframes
    """
    @staticmethod
    def a_column_changed(row1, row2, columns):
        a_column_changed = False
        for col in columns:
            a_column_changed = a_column_changed or row1[col] is not row2[col]
        return a_column_changed

    @staticmethod
    def player_appeared(row1, row2, columns=['players', 'killed']):
        player_appeared = False
        for col in columns:
            player_appeared = player_appeared or any(not element in row1[col] for element in row2[col])
        return player_appeared

    @staticmethod
    def player_disappeared(row1, row2, columns=['players', 'killed']):
        return Log.player_appeared(row2, row1, columns)