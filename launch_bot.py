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

if __name__ == '__main__':

    start_time = time.time()
    
    bot = Bot('src/img/new_walkable_small.png', 
            want_to_read_tasks=False, 
            want_to_detect_players=False,
            want_to_connect_discord=True,
            debug_mode=False)
    
    # print(VisionManager().start_detect_players())
    # while(VisionManager().is_detect_players_running()):
    #     time.sleep(1)

    bot.vision_manager.event_handler.fire('language_wantToSay', f"Attention, j'arriiive ({time.time() - start_time:.1f} secondes)")
    time.sleep(5)

    bot.run()