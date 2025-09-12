import enum

class CompleteStatus(str, enum.Enum):
    COMPLETED = 'completed'
    IN_PROGRESS = 'in progress'
    EMPTY = 'empty'



class UserRoles(str, enum.Enum):
    BASE = 'basic_role'
    ADMIN = 'admin_role'
    SUPER_ADMIN = 'super_admin_role'