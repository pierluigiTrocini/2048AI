from xml.sax import handler
from embasp.languages.predicate import Predicate
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.languages.asp.asp_mapper import ASPMapper
from embasp.languages.asp.asp_input_program import ASPInputProgram
from embasp.languages.asp.answer_sets import AnswerSet, AnswerSets
import numpy

class AIManager:
    def __init__(self) -> None:
        self.SOLVER_PATH = "./dlv-2"

    def generateFacts(self, grid: numpy.array) -> list:
        '''
            Generation Process:
            from Python syntax: grid[row][col] = value 
            to ASP fact: cell(row, col, value).
        '''
        facts = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                facts.append(self.Cell(row = i, col = j, value = grid[i][j]))
        
        return facts
    

    def AIMove(self, grid: numpy.array):
        '''
            Move computing steps:
            1) facts generation (convert grid id ASP facts)
            2) DLV2 execution
            3) return move
        '''


    


    class Cell(Predicate):
        predicate_name = "cell"

        def __init__(self, row: int, col: int, value: int):
            Predicate.__init__(self, [("row", int), ("col", int), ("value", int)])
            
            self.row = row
            self.col = col
            self.value = value
        
        def get_row(self):
            return self.row
        
        def get_col(self):
            return self.col
        
        def get_value(self):
            return self.value
        
        def set_row(self, r: int):
            self.row = r
        
        def set_col(self, c: int):
            self.col = c
        
        def set_value(self, v: int):
            self.value = v
        
        def __str__(self) -> str:
            return f"{self.predicate_name}({self.row},{self.col},{self.value})."

