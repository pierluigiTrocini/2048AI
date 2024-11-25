from xml.sax import handler
from embasp.languages.predicate import Predicate
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.languages.asp.asp_mapper import ASPMapper
from embasp.languages.asp.asp_input_program import ASPInputProgram
from embasp.base.option_descriptor import OptionDescriptor
from embasp.languages.asp.answer_sets import AnswerSet, AnswerSets
import numpy

class AIManager:
    SOLVER_PATH: str = "./dlv-2"
    ASP_RULES_PATH: str = "./transition_function.asp"

    def __init__(self) -> None:
        pass

    def generateFacts(self, grid: numpy.array) -> list:
        '''
            Generation Process:
            from Python syntax: grid[row][col] = value 
            to ASP fact: cell(row, col, value).
        '''
        facts = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                facts.append(self.Cell(row = i, col = j, value = int(grid[i][j])))
        
        return facts
    

    def AIMove(self, grid: numpy.array) -> str:
        '''
            Move computing steps:
            1) facts generation (convert grid id ASP facts)
            2) DLV2 execution
            3) return move
        '''
        handler = DesktopHandler(DLV2DesktopService(self.SOLVER_PATH))
        
        ASPMapper.get_instance().register_class(self.Move)
        ASPMapper.get_instance().register_class(self.Cell)

        inputProgram = ASPInputProgram()
        inputProgram.add_files_path(self.ASP_RULES_PATH)
        inputProgram.add_objects_input(self.generateFacts(grid))

        handler.add_program(inputProgram)

        answerSets: AnswerSets = handler.start_sync()

        for answerSet in answerSets.get_answer_sets():
            for atom in answerSet.get_atoms():
                if isinstance(atom, self.Move):
                    print(f"ANSWER SET -> {atom.get_move()}")
                    return atom.get_move()


    class Move(Predicate):
        predicate_name = "move"

        def __init__(self, move = None):
            Predicate.__init__(self, [("move")])
            self.move = move
        
        def get_move(self):
            return self.move
        
        def set_move(self, move):
            self.move = move

        def __str__(self) -> str:
            return f"{self.predicate_name}({self.move})."

    class Cell(Predicate):
        predicate_name = "cell"

        def __init__(self, row = None, col = None, value = None):
            Predicate.__init__(self,[("row", int), ("col", int), ("value", int)]) 

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

