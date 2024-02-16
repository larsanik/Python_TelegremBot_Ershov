def draw_board(board, sze):
    # запустить цикл, который проходит по всем  строкам доски
    for i in range(sze):
        # поставить разделители значений в строке
        print(" | ".join(board[i]))
        # поставить разделители строк
        print("---" * sze + "-" * (sze - 3))

def ask_move(player, board):
    # определяем размер доски
    sze = len(board)
    # дать игроку возможность сделать ход, то есто есть ввести координаты
    x, y = input(f"{player}, Введите x и y координаты (пример 0 0): ").strip().split()
    # преобразовать координаты в целые числа
    x, y = int(x), int(y)
    # задать условие, которое проверяет,
    # находится ли координата в пределах поля и свободно ли место
    if (0 <= x <= (sze-1)) and (0 <= y <= (sze-1)) and (board[x][y] == " "):
        # если свободно, записать значение игрока (Х или 0) в ячейку
        return(x, y)
    else:
        print("Клетка занята. Попробуйте еще раз.")
        return ask_move(player, board)

def make_move(player, board, x, y):
    # прговерить что клетка свободна
    if board[x][y] != " ":
        print('Клетка занята!')
        return False
    # если клетка свободна, записать ход
    board[x][y] = player
    return True

def ask_and_make_move(player, board):
    x, y = ask_move(player, board)
    # координаты x, y взять из функции ask_move(player, board)
    make_move(player, board, x, y)

def check_win(player, board):
    # проверяем не стал ли очередной ход выигрышным
    # определяем размер доски
    sze = len(board)
    # проверяем строки
    for i in range(sze):
        str = ''
        for ii in range(sze):
            str = str + board[i][ii]
        if str == player * sze:
            return True
    # проверяем столбцы
    for i in range(sze):
        str = ''
        for ii in range(sze):
            str = str + board[ii][i]
        if str == player * sze:
            return True
    # проверяем диогональ лв-пн
    str = ''
    for i in range(sze):
        str = str + board[i][i]
    if str == player * sze:
        return True
    # проверяем диогональ лн-пв
    str = ''
    for i in range(sze):
        str = str + board[(sze-1)-i][i]
    if str == player * sze:
        return True

#def tic_tac_toe():


# call for test
sze = 9
board = [[" " for i in range(sze)] for j in range(sze)]
# аналог [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']] - красивое решение с циклами!

#board = (['O', 'X', 'O'],
#         ['X', 'O', 'X'],
#         ['X', 'O', 'X'])
player = 'X'
#print(board)
#draw_board(board)
#ask_and_make_move( 'X', board)
draw_board(board, sze)
print(check_win(player, board))


