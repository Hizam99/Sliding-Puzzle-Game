"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""

from a1_support import *
from typing import Optional
from math import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Hizam Alaklbi>, <46127679>"
__email__ = "<s4612767@student.uq.edu.au>"


def move(puzzle: str, direction: str) -> Optional [str]:
    """
        This function will moves the empty index in the given direction.

        Parameters:
            puzzle (str): Same as the solution except for the last character.
            direction (str): The move need to be implement.
            
        Returns:
            Optional [str]:If the move is valid it returns the updated puzzle
                           and None otherwise.
    """ 
    empty_index = puzzle.index(EMPTY)
    grid_length = int(sqrt(len(puzzle)))
    up_index = empty_index - grid_length
    #the index above the empty_index aimed to move to
    down_index = empty_index + grid_length
    #the index below the empty_index aimed to move to
    
    if direction == UP and empty_index >= grid_length :
            return swap_position(puzzle,empty_index,up_index)
        
    elif direction == DOWN and empty_index <= ((int(len(puzzle)))) - (grid_length):
            return swap_position(puzzle,empty_index,down_index)
    
    elif direction == LEFT and ( empty_index % (grid_length)) != 0:
            return swap_position(puzzle,empty_index,empty_index-1)     
        
    elif direction == RIGHT and empty_index % (grid_length) != (grid_length)-1:
            return swap_position(puzzle,empty_index,empty_index+1) 
    else:
            return None 


def swap_position(puzzle: str, from_index: int, to_index: int):
    """
        This function will swap the positions of the characters at from index
        and to index in the puzzle and returns the updated puzzle.
               
        Parameters:
            puzzle (str): Same as the solution except for the last character.
            from_index (int): The place of the empty tile.
            to_index (int): The new Position that aimed to move to.
        
        Returns:
           (str): The updated puzzle.
    """ 
    if from_index > to_index:
        from_index, to_index = to_index,from_index
    if from_index == to_index:
        return puzzle
  
    new_puzzle = puzzle[0:from_index] + puzzle[to_index] \
        + puzzle[from_index+1:to_index] + puzzle[from_index] + puzzle[to_index+1:]
    return new_puzzle


def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.

    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.

    Returns:
        (str): a solvable shuffled game with an empty tile at the
               bottom right corner.

    References:
        - https://en.wikipedia.org/wiki/15_puzzle#Solvability
        - https://www.youtube.com/watch?v=YI1WqYKHi78&ab_channel=Numberphile

    Note: This function uses the swap_position function that you have to
          implement on your own. Use this function when the swap_position
          function is ready
    """
    shuffled_solution = solution[:-1]
    
        
    # Do more shuffling for bigger puzzles.
    swaps = len(solution) * 2
    for _ in range(swaps):
        # Pick two indices in the puzzle randomly.
        index1, index2 = random.sample(range(len(shuffled_solution)), k=2)
        shuffled_solution = swap_position(shuffled_solution, index1, index2)

    return shuffled_solution + EMPTY


def check_win(puzzle: str, solution: str):
    """
        This function will check if the game is won or not.

        Parameters:
            puzzle (str): Same as the solution except for the last character.
            solution (str): a sloution that being aimed to.
        
        Returns:
           (str): it is going to returns True,given the puzzle and the solution,
                  and False otherwise.
    """
    return puzzle[:-1] == solution[:-1] 

    
def print_grid(puzzle: str) -> None:
    """
        This function will displays the puzzle in a nice format.

        Parameters:
            puzzle(str): Same as the solution except for the last character
                         aimed to be converted to puzzle

        Returns:
            The puzzle in a nice format. 
    """
    divider = CORNER + int(sqrt(len(puzzle)))*(3* HORIZONTAL_WALL + CORNER) 
    size = int(sqrt(len(puzzle)))
    output = ""
    
    for x in range(size):
        output += divider +"\n"
        for y in range (size):
            index = x * size + y
            output1 = ""
            output1 += VERTICAL_WALL + " "+ puzzle[index]+ " "
            output += output1
        output += VERTICAL_WALL    
        output += "\n" 
    print(output + divider)


def restart_game(puzzle:str,solution:str):
    """
        This function will restart the game after a win or after giving up.

        Parameters:
            puzzle(str): New solution need to be solved.
            solution (str): The solution need to be reached.  

        Returns:
           (str): The new puzzle and new solution. 
    """
    number = input(BOARD_SIZE_PROMPT)
    words = len(number)
    solution = get_game_solution('words.txt',int(number))
    puzzle = shuffle_puzzle(solution)
    return puzzle,solution


def printing_puzzle(puzzle:str,solution:str):
    """
        This function will print the solution and the current position of the game.
        
        Parameters:
            puzzle(str): Same as the solution except for the last character in a nice format.
            solution (str): The solution in a nice format.  

        Returns:
            The puzzle and the solution in a grid format.
    """
    print("Solution:")
    print_grid(solution)
    print("\nCurrent position:")
    print_grid(puzzle)

        
# Write your functions here

def main():
    """Entry point to gameplay"""
    print(WELCOME_MESSAGE)
    number = input(BOARD_SIZE_PROMPT)
    words = len(number)
    solution = get_game_solution('words.txt',int(number))
    puzzle = shuffle_puzzle(solution)

    while True:
        printing_puzzle(puzzle,solution)
        print("")
        #checking if the puzzle is being solved at the begining
        answer = check_win(puzzle,solution)
        if answer == True:  
            print("\nCurrent position:")
            print_grid(puzzle)
            print("\n"+WIN_MESSAGE)
            play_again = input(PLAY_AGAIN_PROMPT)
            if play_again in {"y","Y", ""}:
               puzzle, solution = restart_game(puzzle,solution)
               continue
               #new solution and new puzzle
            else:
                print(BYE)
                break
        move_outcome = None
        char = input(DIRECTION_PROMPT)
        if char == "H":
            print(HELP_MESSAGE)

        elif char == "GU":
            print(GIVE_UP_MESSAGE)
            play_again = input(PLAY_AGAIN_PROMPT)
            if play_again in {"y","Y", ""}:
                puzzle, solution = restart_game(puzzle,solution)
            else:
               print(BYE)
               break
        elif char in {UP,DOWN, LEFT, RIGHT}:
            move_outcome = move(puzzle, char)

            if move_outcome == None:
                print(INVALID_MOVE_FORMAT.format(char))
            else:
                puzzle = move_outcome
            # move outcome can be none or a new puzzle
        else:
            print(INVALID_MESSAGE)  
        answer = check_win(puzzle,solution)
        if answer == True:
            printing_puzzle(puzzle,solution)
            print("\n"+WIN_MESSAGE)
            play_again = input(PLAY_AGAIN_PROMPT)
            if play_again in {"y","Y", ""}:
               puzzle, solution = restart_game(puzzle,solution)
               continue 
            else:
                print(BYE)
                break

        char = ""
            
    
if __name__ == "__main__":
    main()
