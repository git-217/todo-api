import enum

class CompleteStatus(str, enum.Enum):
    COMPLETED = 'COMPLETED'
    IN_PROGRESS = 'IN_PROGRESS'



class Role(str, enum.Enum):
    BASE = 'base'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'