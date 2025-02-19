from enum import Enum
import sys
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

EXPECTIMINIMAX_DEPTH = 2

def generateCells(grid: numpy.array, move: str):
    facts = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            facts.append(Cell(move = move, row = (i + 1), col = (j + 1), value = int(grid[i][j])))
    
    return facts

def generate_grid(grid: numpy.ndarray, direction: str) -> numpy.ndarray:
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

def generateFacts(grid: numpy.array) -> list:
    '''
        From grid param, calculate the next (max) four grid,
        then pass to DLV as logic facts.
    '''
    facts = []

    # Generate new grids
    moveUp: numpy.array = generate_grid(grid = grid, direction = "u")
    moveDown: numpy.array = generate_grid(grid = grid, direction = "d")
    moveLeft: numpy.array = generate_grid(grid = grid, direction = "l")
    moveRight: numpy.array = generate_grid(grid = grid, direction = "r")

    if not numpy.array_equal(grid, moveUp):
        facts.extend(generateCells(grid = moveUp, move = "u"))
    if not numpy.array_equal(grid, moveDown):
        facts.extend(generateCells(grid = moveDown, move = "d"))
    if not numpy.array_equal(grid, moveLeft):
        facts.extend(generateCells(grid = moveLeft, move = "l"))
    if not numpy.array_equal(grid, moveRight):
        facts.extend(generateCells(grid = moveRight, move = "r"))
    
    facts.extend(generateCells(grid = grid, move = "current"))

    # for f in facts:
    #     print(f.__str__())

    return facts


class AIManager:
    SOLVER_PATH: str = "./dlv-2"
    ASP_RULES_PATH: str = "./transition_function.asp"

    def __init__(self) -> None:
        pass


    def AIMove(self, grid: numpy.array) -> str:
        '''
            Move computing steps:
            1) facts generation (convert grid id ASP facts)
            2) DLV2 execution
            3) return move
        '''
        try:
            handler = DesktopHandler(DLV2DesktopService(self.SOLVER_PATH))
            
            ASPMapper.get_instance().register_class(Move)
            ASPMapper.get_instance().register_class(Cell)

            inputProgram = ASPInputProgram()
            inputProgram.add_files_path(self.ASP_RULES_PATH)
            inputProgram.add_objects_input(generateFacts(grid))

            handler.add_program(inputProgram)

            answerSets: AnswerSets = handler.start_sync()

            if len(answerSets.get_optimal_answer_sets()) != 0:
                optimalAS: AnswerSet = answerSets.get_optimal_answer_sets().pop()

                # print(optimalAS.get_answer_set())

                for atom in optimalAS.get_atoms():
                    if isinstance(atom, Move):
                        move = str(atom.get_move()).replace('"','')
                        print(f"[AI][ANSWER SET] MOSSA -> {move}")
                        print(f"[AI][ANSWER SET] Costi dei constraint -> {optimalAS.get_weights().__str__()}")
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
    

class MinimaxNode():
    class Type(Enum):
        AI_MOVE = 0,
        RANDOM_TILE = 1,

    def __init__(self, grid: numpy.array, state: str, depth: int, type: Type, evaluation: int):
        self.type: MinimaxNode.Type = type
        self.state: str = state
        self.evaluation: dict = self.DLV_Evaluation(grid = grid, state = self.state) if self.type == MinimaxNode.Type.AI_MOVE else {}
        self.depth: int = depth

        self.numeric_evaluation: int = 0
        if self.type == MinimaxNode.Type.AI_MOVE:
            self.numeric_evaluation = sum([key * value for key, value in self.evaluation.items()])
        elif self.type == MinimaxNode.Type.RANDOM_TILE:
            self.numeric_evaluation = evaluation

        with open("output.txt", "a") as f:
            f.write(f"[DEBUG] Type: {self.type} | State: {self.state} | Depth: {self.depth} | Evaluation: {self.evaluation} | Total ev: {self.numeric_evaluation}\n")

        self.children_state: list = []

        if self.type == MinimaxNode.Type.AI_MOVE:
            self.add_children_random_tyle(grid = grid, depth = depth + 1)
        elif self.type == MinimaxNode.Type.RANDOM_TILE:
            self.add_children_move(grid = grid, depth = (depth + 1))
        
    def add_children_random_tyle(self, grid: numpy.array, depth):
        if self.depth < EXPECTIMINIMAX_DEPTH:
            for i in range(N):
                for j in range(N): 
                    if grid[i][j] == 0:
                        new_grid: numpy.array = numpy.copy(grid)
                        new_grid[i][j] = 2
                        self.children_state.append(MinimaxNode(new_grid, "", depth, MinimaxNode.Type.RANDOM_TILE, 9))

                        new_grid = numpy.copy(grid)
                        new_grid[i][j] = 4
                        self.children_state.append(MinimaxNode(new_grid, "", depth, MinimaxNode.Type.RANDOM_TILE, 1))


    def add_children_move(self, grid: numpy.array, depth):
        if self.depth < EXPECTIMINIMAX_DEPTH:
            for move in ["u", "d", "l", "r"]:
                new_grid = generate_grid(grid = grid, direction = move)
                if not numpy.array_equal(grid, new_grid):
                    self.children_state.append(MinimaxNode(grid = new_grid, state = move, depth = depth, type = MinimaxNode.Type.AI_MOVE, evaluation = 0))

    
    def DLV_Evaluation(self, grid: numpy.array, state: str):
        try:
            handler = DesktopHandler(DLV2DesktopService(AIManager.SOLVER_PATH))

            ASPMapper.get_instance().register_class(Move)
            ASPMapper.get_instance().register_class(Cell)

            inputProgram = ASPInputProgram()
            inputProgram.add_files_path(AIManager.ASP_RULES_PATH)
            inputProgram.add_objects_input(generateCells(grid = grid, move = state))

            handler.add_program(inputProgram)        

            answerSets: AnswerSets = handler.start_sync()

            if len(answerSets.get_optimal_answer_sets()) != 0:
                optimalAS: AnswerSet = answerSets.get_optimal_answer_sets().pop()

                for atom in optimalAS.get_atoms():
                    if isinstance(atom, Move):
                        move = str(atom.get_move()).replace('"','')
                        if move != self.state:
                            raise Exception(f"[DEBUG] move e state non coincidono. move = {move} | state = {self.state}")
                        
                        return optimalAS.get_weights()
            else:
                print(f"[AI][WARNING] Il modulo AI non ha prodotto risultati")
                return {}
        finally:
            inputProgram.clear_all()
       
