#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
最小最大AI算法在井字游戏中的实现，使用Python3

为了使用AI解决游戏，我们将介绍游戏树的概念，然后是最小最大值算法。游戏的不同状态由游戏树中的节点表示，与规划问题非常相似。
这个想法只是略有不同。在游戏树中，节点排列在对应于游戏中每个玩家回合的关卡中，因此树的“根”节点（通常描绘在图表的顶部）是游
戏中的起始位置。在井字游戏中，这将是尚未播放X或O的空网格。在根下，在第二级，第一个玩家的移动可能导致可能的状态，无论是 X 
还是 O。我们将这些节点称为根节点的“子节点”。

第二层的每个节点将进一步具有对方玩家的移动可以从中到达的状态作为其子节点。这种情况会逐级持续，直到达到游戏结束的状态。在井
字游戏中，这意味着其中一名玩家获得三分线并获胜，或者棋盘已满并且游戏以平局结束。

什么是最大最小值？

Minimax是一种应用于双人游戏的人工智能，例如井字游戏，跳棋，国际象棋和围棋。这种游戏被称为零和游戏，因为在数学表示中：一个
玩家赢（+1），另一个玩家输（-1）或两个人都不赢（0）。

算法递归搜索导致Max玩家赢或不输（平局）的最佳动作。它考虑游戏的当前状态和该状态下的可用移动，然后对于它玩的每个有效移动
（交替最小和最大），直到它找到最终状态（赢、平或输）。

"""

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    此函数测试特定玩家是否获胜。可能性:
    *三行[X X X]或[O O O]
    *三列[X X X]或[O O O]
    *两条对角线[X X X]或[O O O]
    :param state:当前板的状态
    :param player:人或计算机
    :return:如果玩家获胜则为True
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    这个功能测试是人类还是计算机获胜
    :param state:当前板的状态
    :return:如果人类或计算机获胜则为True

    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    每个空单元格将被添加到单元格列表中
    :param state:当前板的状态
    :return:空单元格列表

    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    如果所选单元格为空，则移动有效
    :参数x: x坐标
    :参数y: y坐标
    :return:如果板[x][y]为空则为True

    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    如果坐标有效，就在船上设置移动
    :参数x: x坐标
    :参数y: y坐标
    :param player:当前玩家

    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI功能，选择最佳的移动
    :param state:当前单板状态
    :参数depth:树中的节点索引(0 <= depth <= 9)，
    但在这种情况下绝不是9(参见iaturn()函数)
    :param player:人或计算机
    :return:一个包含[最佳行，最佳col，最佳分数]的列表

    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    清除控制台

    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    在控制台打印单板
    :param state:当前单板状态

    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    如果深度< 9，则调用minimax函数，
    否则它选择一个随机的坐标。
    :参数c_choice:计算机的选择X或O
    :param h_choice:人的选择X或O
    :return
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    人类选择一个有效的行动。
    :参数c_choice:计算机的选择X或O
    :param h_choice:人的选择X或O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # 有效招数存入字典，这样处理优化了输入
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    调用所有函数的main函数
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # 玩家选择使用X或者O
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # 设置计算机的选择
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # 玩家选择是否先手
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # 此游戏的主循环
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # 游戏结束消息
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')
    play_again = input("The game is over. Do you want to play again? (Y/N)")

    if play_again.upper() == "Y":
        # 重新开始游戏
        main()
    elif play_again.upper() == "N":
        exit()
    else:
        print("Invalid input, please enter Y or N.")
    exit()


if __name__ == '__main__':
    main()
