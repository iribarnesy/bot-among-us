from enum import Enum

class TasksTexts(Enum):
    SABOTAGE_O2 = "Oxygen Depleted"
    SABOTAGE_LIGHTS = "Fix Lights"
    SABOTAGE_COMMS = "Comms Sabotaged"
    SABOTAGE_REACTOR = "Reactor Meltdown"

    @classmethod
    def get_sabotage_texts(cls):
        return [
            cls.SABOTAGE_O2,
            cls.SABOTAGE_LIGHTS,
            cls.SABOTAGE_COMMS,
            cls.SABOTAGE_REACTOR
        ]
