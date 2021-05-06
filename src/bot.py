from src.tasks import TaskType, Task, TaskManager
from src.game_map import SkeldMap
from src.position import Position, Directions
from src.vision import VisionManager, GamePhase
from src.enums.texts import TasksTexts
from src.navigation import NavigationManager, MovingAction
from src.brain import BrainManager
from src.discord_bot import DiscordBot

class Bot:
    def __init__(self, 
                 map_img_path='src/img/new_walkable_small.png',
                 want_to_read_tasks=True,
                 want_to_detect_players=True,
                 want_to_connect_discord=True,
                 debug_mode=True):
        self.name = "Le bot"
        self.game_map = SkeldMap(map_img_path)
        self.vision_manager = VisionManager(want_to_read_tasks=want_to_read_tasks, want_to_detect_players=want_to_detect_players, debug_mode=debug_mode)
        self.position = Position()
        
        self.brain_manager = BrainManager(self.position, vision_manager=self.vision_manager)
        
        if want_to_connect_discord:
            self.discord_bot = DiscordBot()
            self.discord_bot.start_listening()

    def run(self, 
            react_to_events=True, blacklist_events=[], 
            connect_to_discord=True):
        if react_to_events:
            self.brain_manager.connect_events(blacklist_events)
        self.vision_manager.init_event_values()
        self.vision_manager.start_vision_loop()
    
    def stop(self):
        self.vision_manager.stop_vision_loop()
        self.brain_manager.stop_sabotage_resolution_thread()
        self.brain_manager.stop_tasks_resolution_thread()
