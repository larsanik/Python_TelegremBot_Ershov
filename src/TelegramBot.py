def draw_board(board):
    # запустить цикл, который проходит по всем 3 строкам доски
    print(board)
    for i in range(3):
        # поставить разделители значений в строке
        print(" | ".join(board[i]))
        # поставить разделители строк
        print("---------")

def ask_and_make_move(player, board):
    # дать игроку возможность сделать ход, то есто есть ввести координаты
    x, y = input(f"{player}, enter x and y coordinates (e.g. 0 0): ").strip().split()
    # преобразовать координаты в целые числа
    x, y = int(x), int(y)
    # задать условие, которое проверяет,
    # находится ли координата в пределах поля и свободно ли место
    if (0 <= x <= 2) and (0 <= y <= 2) and (board[x][y] == " "):
        # если свободно, записать значение игрока (Х или 0) в ячейку
        board[x][y] = player
    else:
        print("That spot is already taken. Try again.")

board = [[" " for i in range(3)] for j in range(3)] # аналог [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']] - красивое решение!


# call for test
board[0][0] = 'X'
print(board)
draw_board(board)
ask_and_make_move( 'X', board)


