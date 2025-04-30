import subprocess
import shutil
import chess.pgn
from io import StringIO

def read_clipboard_text():
    try:
        text_data = subprocess.check_output(["wl-paste", "--type", "text/plain"], stderr=subprocess.DEVNULL, text=True)
        return text_data
    except subprocess.CalledProcessError:
        return None

def main():
    while True:
        print("Press Enter to paste PGN of a game!")

        try:
            _ = input()
        except EOFError:
            break
        
        text = read_clipboard_text()
        if text:
            print("PGN successfully pasted!")

            pgn_io = StringIO(text)
            game = chess.pgn.read_game(pgn_io)

            print("PGN successfully formated!")

            board = game.board()
            moves = list(game.mainline_moves())

            terminal_width = shutil.get_terminal_size().columns
            print("Formated PGN:")
            print("=" * terminal_width)

            for i in range(0, len(moves), 2):
                move_number = i//2 + 1
                white_san = board.san(moves[i])
                board.push(moves[i])

                if i+1 < len(moves):
                    black_san = board.san(moves[i+1])
                    board.push(moves[i+1])
                else:
                    black_san = ""

                print(f"{move_number}. {white_san} {black_san}")

            print("=" * terminal_width)
        else:
            print("No PGN found in the clipboard!")

if __name__ == "__main__":
    main()