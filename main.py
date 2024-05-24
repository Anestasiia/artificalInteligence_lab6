from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.core.window import Window


class TicTacToeBoard:
    def __init__(self):
        self.board = [0] * 9

    def make_move(self, position, player):
        if self.board[position] == 0:
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_combinations:
            if self.board[a] == self.board[b] == self.board[c] != 0:
                return self.board[a]
        if 0 not in self.board:
            return 'draw'
        return None


class TicTacToeApp(App):
    def build(self):
        self.title = 'Tic-Tac-Toe'
        self.board = TicTacToeBoard()
        # Player first
        self.current_player = 1
        # AI first
        # self.current_player = 2
        self.layout = GridLayout(cols=3)
        self.buttons = []

        for i in range(9):
            button = Button(font_size=24, color='white')
            button.width = 130
            button.height = 130
            button.background_color = 'white'
            button.bind(on_press=self.button_pressed)
            self.layout.add_widget(button)
            self.buttons.append(button)

        # AI first
        # self.run_ai()
        return self.layout

    def button_pressed(self, instance):
        position = self.buttons.index(instance)
        if self.board.make_move(position, self.current_player):
            # Player first
            instance.text = 'x' if self.current_player == 2 else 'o'
            # AI first
            # instance.text = 'o' if self.current_player == 2 else 'x'
            winner = self.board.check_winner()
            if winner:
                self.show_winner(winner)
                return
            self.current_player = 3 - self.current_player
            if self.current_player == 2:
                self.run_ai()

    def run_ai(self):
        best_move = self.minimax(self.board, True)[1]
        if best_move is not None:
            self.button_pressed(self.buttons[best_move])

    def minimax(self, board, maximizing):
        winner = board.check_winner()
        if winner:
            if winner == 'draw':
                return 0, None
            else:
                return (1 if winner == 2 else -1, None)

        if maximizing:
            best_value = -1
            best_move = None
            for move in range(9):
                if board.board[move] == 0:
                    board.board[move] = 2
                    #Перемога гравця
                    value = self.minimax(board, True)[0]
                    #Перемога ШІ
                    # value = self.minimax(board, False)[0]

                    board.board[move] = 0
                    if value > best_value:
                        best_value = value
                        best_move = move
            return best_value, best_move
        else:
            best_value = 1
            best_move = None
            for move in range(9):
                if board.board[move] == 0:
                    board.board[move] = 1
                    # Перемога гравця
                    value = self.minimax(board, False)[0]
                    # Перемога ШІ
                    # value = self.minimax(board, True)[0]

                    board.board[move] = 0
                    if value < best_value:
                        best_value = value
                        best_move = move
            return best_value, best_move

    def show_winner(self, winner):
        view = ModalView(size_hint=(0.5, 0.25))
        if winner == 'draw':
            winner_label = Label(text='Draw', font_size=24, color='white')
            view.background_color = 'grey'
        elif winner == 2:
            winner_label = Label(text=f'Opponent win', font_size=24, color='red',
                                 outline_color=get_color_from_hex('#00FF00'))
            view.background_color = 'red'
        else:
            winner_label = Label(text=f'You win', font_size=24, color='green',
                                 outline_color=get_color_from_hex('#00FF00'))
            view.background_color = 'green'
        view.add_widget(winner_label)
        view.bind(on_dismiss=self.reset_game)
        view.open()

    def reset_game(self, instance):
        self.board = TicTacToeBoard()
        for button in self.buttons:
            button.text = ''
        # Player first
        self.current_player = 1
        # AI first
        # self.current_player = 2
        # self.run_ai()


if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (300, 300)
    TicTacToeApp().run()
