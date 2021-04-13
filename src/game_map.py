from src.tasks import TaskManager, TaskType, Task
from src.navigation import NavigationManager
class SkeldMap(TaskManager):
    def __init__(self, map_image_path):
        self.map_image_path = map_image_path
        self.navigationManager = NavigationManager(self.map_image_path) 
        self.tasks = [
            Task(0, "Align Engine (Upper Engine)", (273, 355), indicator_location=(130, 179), solve_function=self.align_engine_output, task_type=TaskType.Align_Engine_Output),
            Task(1, "Align Engine (Lower Engine)", (275, 854), indicator_location=(133, 425), solve_function=self.align_engine_output, task_type=TaskType.Align_Engine_Output),
            Task(2, "Calibrate Distributor", (817, 643), indicator_location=(410, 323), solve_function=self.calibrate_distributor, task_type=TaskType.Calibrate_Distributor),
            Task(3, "Chart Course", (1796, 432), indicator_location=(903, 236), solve_function=self.chart_course, task_type=TaskType.Chart_Course),
            Task(4, "Clean O2 Filter", (1293, 460), indicator_location=(635, 228), solve_function=self.clean_O2_filter, task_type=TaskType.Clean_O2_Filter),
            Task(5, "Clear Asteroids", (1430, 262), indicator_location=(707, 123), solve_function=self.clear_asteroids, task_type=TaskType.Clear_Asteroids),
            Task(6, "Divert Power", (690, 635), indicator_location=(328, 315), solve_function=self.divert_power, task_type=TaskType.Divert_Power),
            Task(7, "Accept Power (Communications)", (1310, 914), indicator_location=(656, 461), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(8, "Accept Power (Lower Engine)", (322, 717), indicator_location=(157, 356), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(9, "Accept Power (Upper Engine)", (352, 209), indicator_location=(172, 105), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(10, "Accept Power (Navigation)", (1712, 437), indicator_location=(860, 211), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(11, "Accept Power (O2)", (1400, 441), indicator_location=(705, 216), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(12, "Accept Power (Security)", (562, 462), indicator_location=(274, 224), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(13, "Accept Power (Shields)", (1496, 763), indicator_location=(745, 375), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(14, "Accept Power (Weapons)", (1525, 252), indicator_location=(760, 123), solve_function=self.accept_power, task_type=TaskType.Accept_Power),
            Task(15, "Empty Garbage/Chute (Cafeteria)", (1241, 176), indicator_location=(623, 81), solve_function=self.empty_chute, task_type=TaskType.Empty_Chute),
            Task(16, "Empty Garbage/Chute (O2)", (1260, 473), indicator_location=(635, 239), solve_function=self.empty_chute, task_type=TaskType.Empty_Chute),
            Task(17, "Empty Garbage/Chute (Storage)", (1092, 1020), indicator_location=(534, 519), solve_function=self.empty_chute, task_type=TaskType.Empty_Chute),
            Task(18, "Fix Wires (Electrical)", (742, 651), indicator_location=(368, 328), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(19, "Fix Wires (Storage)", (978, 696), indicator_location=(475, 343), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(20, "Fix Wires (Security)", (422, 528), indicator_location=(201, 255), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(21, "Fix Wires (Navigation)", (1652, 492), indicator_location=(801, 241), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(22, "Fix Wires (Admin)", (1114, 599), indicator_location=(534, 284), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(23, "Fix Wires (Cafeteria)", (841, 124), indicator_location=(421, 62), solve_function=self.fix_wires, task_type=TaskType.Fix_Wires),
            Task(24, "Fuel Engine (Storage)", (941, 906), indicator_location=(465, 450), solve_function=self.fuel_engines, task_type=TaskType.Fuel_Engines),
            Task(25, "Fuel Engine (Lower Engine)", (308, 852), indicator_location=(150, 425), solve_function=self.fuel_engines, task_type=TaskType.Fuel_Engines),
            Task(26, "Fuel Engine (Upper Engine)", (308, 350), indicator_location=(146, 175), solve_function=self.fuel_engines, task_type=TaskType.Fuel_Engines),
            Task(27, "Inspect Sample", (808, 513), indicator_location=(394, 253), solve_function=self.inspect_sample, task_type=TaskType.Inspect_Sample),
            Task(28, "Prime Shields", (1367, 910), indicator_location=(684, 459), solve_function=self.prime_shields, task_type=TaskType.Prime_Shields),
            Task(29, "Stabilize Steering", (1824, 532), indicator_location=(903, 261), solve_function=self.stabilize_steering, task_type=TaskType.Stabilize_Steering),
            Task(30, "Start Reactor", (166, 565), indicator_location=(78, 271), solve_function=self.start_reactor, task_type=TaskType.Start_Reactor),
            Task(31, "Submit Scan", (757, 552), indicator_location=(360, 268), solve_function=self.submit_scan, task_type=TaskType.Submit_Scan),
            Task(32, "Swipe Card", (1289, 691), indicator_location=(635, 337), solve_function=self.swipe_card, task_type=TaskType.Swipe_Card),
            Task(33, "Unlock Manifolds", (135, 440), indicator_location=(60, 213), solve_function=self.unlock_manifold, task_type=TaskType.Unlock_Manifold),
            Task(34, "Download/Upload (Cafeteria)", (1200, 137), indicator_location=(601, 55), solve_function=self.download_upload, task_type=TaskType.Download_Upload),
            Task(35, "Download/Upload (Admin)", (1160, 593), indicator_location=(552, 284), solve_function=self.download_upload, task_type=TaskType.Download_Upload),
            Task(36, "Download/Upload (Communications)", (1215, 908), indicator_location=(589, 453), solve_function=self.download_upload, task_type=TaskType.Download_Upload),
            Task(37, "Download/Upload (Electrical)", (655, 585), indicator_location=(317, 323), solve_function=self.download_upload, task_type=TaskType.Download_Upload),
            Task(38, "Download/Upload (Navigation)", (1752, 438), indicator_location=(860, 211), solve_function=self.download_upload, task_type=TaskType.Download_Upload),
            Task(39, "Download/Upload (Weapons)", (1413, 177), indicator_location=(694, 86), solve_function=self.download_upload, task_type=TaskType.Download_Upload)
        ]