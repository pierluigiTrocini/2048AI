from embasp.languages.predicate import Predicate
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.languages.asp.asp_mapper import ASPMapper
from embasp.languages.asp.asp_input_program import ASPInputProgram
from embasp.base.option_descriptor import OptionDescriptor
from embasp.languages.asp.answer_sets import AnswerSet, AnswerSets
import numpy

import random

N = 4

class AIManager:
    SOLVER_PATH: str = "./dlv-2"
    ASP_RULES_PATH: str = "./transition_function.asp"

    def __init__(self) -> None:
        pass

    def generateFacts(self, grid: numpy.array) -> list:
        '''
            From grid param, calculate the next (max) four grid,
            then pass to DLV as logic facts.
        '''
        facts = []

        def generateCells(grid, move: str):
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    facts.append(self.Cell(move = move, row = i, col = j, value = int(grid[i][j])))

        # Generate new grids
        moveUp: numpy.array = self.generate_grid(grid = grid, direction = "u")
        moveDown: numpy.array = self.generate_grid(grid = grid, direction = "d")
        moveLeft: numpy.array = self.generate_grid(grid = grid, direction = "l")
        moveRight: numpy.array = self.generate_grid(grid = grid, direction = "r")

        if not numpy.array_equal(grid, moveUp):
            generateCells(grid = moveUp, move = "u")
        if not numpy.array_equal(grid, moveDown):
            generateCells(grid = moveDown, move = "d")
        if not numpy.array_equal(grid, moveLeft):
            generateCells(grid = moveLeft, move = "l")
        if not numpy.array_equal(grid, moveRight):
            generateCells(grid = moveRight, move = "r")
        
        generateCells(grid = grid, move = "current")

        # for f in facts:
        #     print(f.__str__())

        return facts


    def AIMove(self, grid: numpy.array) -> str:
        '''
            Move computing steps:
            1) facts generation (convert grid id ASP facts)
            2) DLV2 execution
            3) return move
        '''
        try:
            handler = DesktopHandler(DLV2DesktopService(self.SOLVER_PATH))
            
            ASPMapper.get_instance().register_class(self.Move)
            ASPMapper.get_instance().register_class(self.Cell)

            inputProgram = ASPInputProgram()
            inputProgram.add_files_path(self.ASP_RULES_PATH)
            inputProgram.add_objects_input(self.generateFacts(grid))

            handler.add_program(inputProgram)

            answerSets: AnswerSets = handler.start_sync()

            if len(answerSets.get_optimal_answer_sets()) != 0:
                optimalAS: AnswerSet = answerSets.get_optimal_answer_sets().pop()

                # print(optimalAS.get_answer_set())

                for atom in optimalAS.get_atoms():
                    if isinstance(atom, self.Move):
                        move = str(atom.get_move()).replace('"','')
                        print(f"[AI][ANSWER SET] MOSSA -> {move}")
                        return move
            else:
                print(f"[AI][WARNING] Il modulo AI non ha prodotto risultati")
                return ""

        finally:
            inputProgram.clear_all()
        


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

        def __init__(self, row = None, col = None, value = None, move = None):
            Predicate.__init__(self,[("move"), ("row", int), ("col", int), ("value", int)]) 

            self.move = move
            self.row = row
            self.col = col
            self.value = value
        
        def get_move(self):
            return self.move
        
        def get_row(self):
            return self.row
        
        def get_col(self):
            return self.col
        
        def get_value(self):
            return self.value
    
        def set_move(self, m: str):
            self.move = m
        
        def set_row(self, r: int):
            self.row = r
        
        def set_col(self, c: int):
            self.col = c
        
        def set_value(self, v: int):
            self.value = v
        
        def __str__(self) -> str:
            return f'{self.predicate_name}("{self.get_move()}",{self.get_row()},{self.get_col()},{self.get_value()}).'

    def generate_grid(self, grid: numpy.ndarray, direction: str) -> numpy.ndarray:
        def compress_and_merge(row):
            non_zero = row[row != 0]
            merged = []
            skip = False

            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                    merged.append(non_zero[i] * 2)
                    skip = True
                else:
                    merged.append(non_zero[i])

            return numpy.array(merged + [0] * (len(row) - len(merged)))

        def process(grid, reverse=False):
            result = []
            for row in grid:
                if reverse:
                    row = row[::-1]
                processed_row = compress_and_merge(row)
                if reverse:
                    processed_row = processed_row[::-1]
                result.append(processed_row)
            return numpy.array(result)

        if direction == "l":
            return process(grid)
        elif direction == "r":
            return process(grid, reverse=True)
        elif direction == "u":
            return process(grid.T).T
        elif direction == "d":
            return process(grid.T, reverse=True).T