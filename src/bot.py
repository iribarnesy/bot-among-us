from src.tasks import TaskType, Task, TaskManager
from src.game_map import SkeldMap
from src.position import Position, Directions
from src.vision import VisionManager, GamePhase
from src.enums.texts import TasksTexts
from src.navigation import NavigationManager, MovingAction
from src.brain import BrainManager

class Bot:
    def __init__(self, map_img_path='src/img/WalkableMesh_resize_small.png'):
        self.name = "Le bot"
        self.game_map = SkeldMap(map_img_path)
        self.vision_manager = VisionManager()
        self.position = Position()
        
        self.brain_manager = BrainManager(self.position, vision_manager=self.vision_manager)

    def run(self, react_to_events=True, blacklist_events=[]):
        if react_to_events:
            self.brain_manager.connect_events(blacklist_events)
        self.vision_manager.start_vision_loop()
    
    def stop(self):
        self.vision_manager.stop_vision_loop()
        self.brain_manager.stop_sabotage_resolution_thread()
        self.brain_manager.stop_tasks_resolution_thread()

if __name__ == '__main__':
    b = Bot()
    b.run()
