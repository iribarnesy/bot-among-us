from shapely.geometry import Polygon

from src.tasks import TaskManager, TaskType, Task
from src.navigation import NavigationManager
from src.room import Room

class SkeldMap():
    def __init__(self, map_image_path):
        self.map_image_path = map_image_path
        self.taskManager = TaskManager()
        self.navigationManager = NavigationManager(self.map_image_path) 
        self.taskManager.tasks = [
            Task(0, "Align Engine (Upper Engine)", (273, 371), indicator_location=(273, 355), solve_function=self.taskManager.align_engine_output, task_type=TaskType.Align_Engine_Output, time_to_fake = 3),
            Task(1, "Align Engine (Lower Engine)", (288, 865), indicator_location=(275, 854), solve_function=self.taskManager.align_engine_output, task_type=TaskType.Align_Engine_Output, time_to_fake = 3),
            Task(2, "Calibrate Distributor", (817, 659), indicator_location=(817, 643), solve_function=self.taskManager.calibrate_distributor, task_type=TaskType.Calibrate_Distributor, time_to_fake = 6),
            Task(3, "Chart Course", (1764, 456), indicator_location=(1796, 432), solve_function=self.taskManager.chart_course, task_type=TaskType.Chart_Course, time_to_fake = 3),
            Task(4, "Clean O2 Filter", (1293, 460), indicator_location=(1293, 460), solve_function=self.taskManager.clean_O2_filter, task_type=TaskType.Clean_O2_Filter, time_to_fake = 13),
            Task(5, "Clear Asteroids", (1430, 278), indicator_location=(1430, 262), solve_function=self.taskManager.clear_asteroids, task_type=TaskType.Clear_Asteroids, time_to_fake = 14),
            Task(6, "Divert Power", (690, 651), indicator_location=(691, 613), solve_function=self.taskManager.divert_power, task_type=TaskType.Divert_Power, time_to_fake = 3),
            Task(7, "Accept Power (Communications)", (1310, 914), indicator_location=(1311, 892), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(8, "Accept Power (Lower Engine)", (322, 717), indicator_location=(322, 717), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(9, "Accept Power (Upper Engine)", (352, 209), indicator_location=(352, 209), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(10, "Accept Power (Navigation)", (1712, 437), indicator_location=(1712, 437), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(11, "Accept Power (O2)", (1398, 445), indicator_location=(1400, 441), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(12, "Accept Power (Security)", (551, 460), indicator_location=(564, 442), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(13, "Accept Power (Shields)", (1468, 742), indicator_location=(1498, 732), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(14, "Accept Power (Weapons)", (1503, 246), indicator_location=(1525, 252), solve_function=self.taskManager.accept_power, task_type=TaskType.Accept_Power, time_to_fake = 3),
            Task(15, "Empty Garbage/Chute (Cafeteria)", (1221, 168), indicator_location=(1241, 176), solve_function=self.taskManager.empty_chute, task_type=TaskType.Empty_Chute, time_to_fake = 6),
            Task(16, "Empty Garbage/Chute (O2)", (1260, 473), indicator_location=(1260, 473), solve_function=self.taskManager.empty_chute, task_type=TaskType.Empty_Chute, time_to_fake = 6),
            Task(17, "Empty Garbage/Chute (Storage)", (1077, 1010), indicator_location=(1092, 1020), solve_function=self.taskManager.empty_chute, task_type=TaskType.Empty_Chute, time_to_fake = 6),
            Task(18, "Fix Wires (Electrical)", (742, 651), indicator_location=(742, 651), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(19, "Fix Wires (Storage)", (978, 696), indicator_location=(981, 674), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(20, "Fix Wires (Security)", (422, 528), indicator_location=(422, 528), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(21, "Fix Wires (Navigation)", (1652, 508), indicator_location=(1652, 492), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(22, "Fix Wires (Admin)", (1107, 606), indicator_location=(1114, 599), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(23, "Fix Wires (Cafeteria)", (841, 124), indicator_location=(841, 124), solve_function=self.taskManager.fix_wires, task_type=TaskType.Fix_Wires, time_to_fake = 4),
            Task(24, "Fuel Engine (Storage)", (941, 906), indicator_location=(941, 906), solve_function=self.taskManager.fuel_engines, task_type=TaskType.Fuel_Engines, time_to_fake = 7),
            Task(25, "Fuel Engine (Lower Engine)", (308, 852), indicator_location=(308, 852), solve_function=self.taskManager.fuel_engines, task_type=TaskType.Fuel_Engines, time_to_fake = 7),
            Task(26, "Fuel Engine (Upper Engine)", (308, 350), indicator_location=(308, 350), solve_function=self.taskManager.fuel_engines, task_type=TaskType.Fuel_Engines, time_to_fake = 7),
            Task(27, "Inspect Sample", (775, 495), indicator_location=(808, 513), solve_function=self.taskManager.inspect_sample, task_type=TaskType.Inspect_Sample, time_to_fake = 3),
            Task(28, "Prime Shields", (1367, 910), indicator_location=(1367, 910), solve_function=self.taskManager.prime_shields, task_type=TaskType.Prime_Shields, time_to_fake = 3),
            Task(29, "Stabilize Steering", (1798, 542), indicator_location=(1824, 532), solve_function=self.taskManager.stabilize_steering, task_type=TaskType.Stabilize_Steering, time_to_fake = 3),
            Task(30, "Start Reactor", (166, 565), indicator_location=(166, 565), solve_function=self.taskManager.start_reactor, task_type=TaskType.Start_Reactor, time_to_fake = 23),
            Task(31, "Submit Scan", (754, 534), indicator_location=(757, 552), solve_function=self.taskManager.submit_scan, task_type=TaskType.Submit_Scan, time_to_fake = 12),
            Task(32, "Swipe Card", (1289, 691), indicator_location=(1289, 691), solve_function=self.taskManager.swipe_card, task_type=TaskType.Swipe_Card, time_to_fake = 6),
            Task(33, "Unlock Manifolds", (135, 440), indicator_location=(135, 440), solve_function=self.taskManager.unlock_manifold, task_type=TaskType.Unlock_Manifold, time_to_fake = 10),
            Task(34, "Download/Upload (Cafeteria)", (1183, 130), indicator_location=(1200, 137), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11),
            Task(35, "Download/Upload (Admin)", (1165, 596), indicator_location=(1160, 593), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11),
            Task(36, "Download/Upload (Communications)", (1215, 924), indicator_location=(1215, 906), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11),
            Task(37, "Download/Upload (Electrical)", (655, 646), indicator_location=(655, 585), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11),
            Task(38, "Download/Upload (Navigation)", (1752, 438), indicator_location=(1752, 438), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11),
            Task(39, "Download/Upload (Weapons)", (1413, 177), indicator_location=(1413, 177), solve_function=self.taskManager.download_upload, task_type=TaskType.Download_Upload, time_to_fake = 11)
        ]
        self.taskManager.sabotages = [
            Task(40, "Sabotage O2 (Admin)", (1326, 600), indicator_location=(1326, 600), solve_function=self.taskManager.sabotage_oxygen, task_type=TaskType.Sabotage_O2),
            Task(41, "Sabotage O2 (O2)", (1333, 448), indicator_location=(1333, 448), solve_function=self.taskManager.sabotage_oxygen, task_type=TaskType.Sabotage_O2),
            Task(42, "Sabotage Com", (1241, 990), indicator_location=(1241, 990), solve_function=self.taskManager.sabotage_communication, task_type=TaskType.Sabotage_Com),
            Task(43, "Sabotage Reactor (High)", (183, 400), indicator_location=(183, 400), solve_function=self.taskManager.sabotage_reactor, task_type=TaskType.Sabotage_Reactor),
            Task(44, "Sabotage Reactor (Low)", (170, 667), indicator_location=(170, 667), solve_function=self.taskManager.sabotage_reactor, task_type=TaskType.Sabotage_Reactor),
            Task(45, "Sabotage_Elec", (660, 750), indicator_location=(660, 746), solve_function=self.taskManager.sabotage_electrical, task_type=TaskType.Sabotage_Elec)
        ]
        self.room = [
            Room("Upper Engine", Polygon([(299,166),(442,166),(442,384),(247,384),(247,213)])),
            Room("Medbay", Polygon([(590,327),(768,327),(768,434),(839,505),(839,560),(625,560),(590,515)])),
            Room("Cafeteria", Polygon([(876,39),(1135,39),(1257,160),(1257,398),(1152,503),(896,504),(791,400),(791,123)])),
            Room("Weapons", Polygon([(1339,137),(1442,137),(1531,225),(1531,354),(1384,354),(1339,314)])),
            Room("O2", Polygon([(1281,383),(1371,383),(1371,528),(1217,529),(1217,467),(1281,398)])),
            Room("Navigation", Polygon([(1689,401),(1769,401),(1838,462),(1838,539),(1769,594),(1689,594)])),
            Room("Shields", Polygon([(1382,715),(1530,715),(1530,844),(1441,935),(1339,935),(1339,759)])),
            Room("Communications", Polygon([(1110,878),(1321,878),(1321,997),(1277,1039),(1154,1039),(1110,998)])),
            Room("Storage", Polygon([(903,659),(1091,659),(1091,1039),(927,1039),(839,953),(839,721)])),
            Room("Admin", Polygon([(1131,556),(1338,556),(1338,707),(1301,745),(1131,745)])),
            Room("Electrical", Polygon([(626,601),(840,601),(840,655),(789,706),(789,790),(745,831),(626,831)])),
            Room("Lower Engine", Polygon([(244,677),(442,677),(442,894),(298,894),(244,853)])),
            Room("Security", Polygon([(490,399),(532,399),(563,431),(563,621),(452,619),(452,438)])),
            Room("Reactor", Polygon([(157,357),(199,357),(199,425),(265,425),(265,622),(199,622),(199,690),(155,690),(82,646),(82,404)]))
        ]