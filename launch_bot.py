import time

from src.bot import *
from src.tasks import *
from src.navigation import *
from src.vision import *
from src.position import *
from src.enums.pixels import *
from src.enums.images import *
from src.enums.texts import *
from src.utils import *
from src.players_recognition.players_detector import *
from src.log import *

def format_sentences_files():
    import os
    for filename in os.listdir('src/data'):
        if filename[-14:] == '.sentences.txt':
            with open('src/data/' + filename, 'r', encoding='utf8') as sentence_file:
                sentences = sentence_file.read().split('\n')
            with open('src/data/' + filename[:-14] + '.text.txt', 'w', encoding='utf8') as text_file:
                text_file.write(". ".join(sentences))

def run_bot_with_detection_and_language():
    start_time = time.time()
    
    bot = Bot('src/img/new_walkable_small.png', 
            want_to_read_tasks=False, 
            want_to_detect_players=True,
            want_to_connect_discord=True,
            debug_mode=False)
    
    print(VisionManager().start_detect_players())
    while(VisionManager().is_detect_players_running()):
        time.sleep(1)

    bot.vision_manager.event_handler.fire('language_wantToSay', f"Attention, j'arriiive ({time.time() - start_time:.1f} secondes)")
    time.sleep(5)

    bot.run()

if __name__ == '__main__':
    run_bot_with_detection_and_language()
#     format_sentences_files()
