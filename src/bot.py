from src.tasks import TaskType, Task, TaskManager
from src.game_map import SkeldMap
from src.position import Position, Directions
from src.vision import VisionManager, GamePhase
from src.enums.texts import TasksTexts
from src.navigation import NavigationManager, MovingAction
from src.brain import BrainManager

class Bot:
    def __init__(self, 
                 map_img_path='src/img/WalkableMesh_resize_small.png',
                 want_to_read_tasks=True,
                 debug_mode=True):
        self.name = "BOTéFATALE"
        self.game_map = SkeldMap(map_img_path)
        self.vision_manager = VisionManager(want_to_read_tasks=want_to_read_tasks, debug_mode=debug_mode)
        self.position = Position()
        self.room = ""
        self.brain_manager = BrainManager(self.position, self.room, vision_manager=self.vision_manager)

    def run(self, react_to_events=True, blacklist_events=[]):
        if react_to_events:
            self.brain_manager.connect_events(blacklist_events)
        self.vision_manager.start_vision_loop()
    
    def stop(self):
        self.vision_manager.stop_vision_loop()
        self.brain_manager.stop_sabotage_resolution_thread()
        self.brain_manager.stop_memorize_room_thread()
        self.brain_manager.stop_tasks_resolution_thread()


if __name__ == '__main__':
    b = Bot()
    b.run()
