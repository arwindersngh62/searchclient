from enum import Enum, unique

@unique
class ConflictEnum(Enum):
    SameCell = 0
    SwappingCells = 1