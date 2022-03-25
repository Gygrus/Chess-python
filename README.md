CHESS

Piotr Socała
Rafał Tekielski

Funkcjonalności aplikacji:
  Umożliwienie lokalnej gry w szachy klasyczne dla dwóch osób
  Zaimplementowanie prawidłowego poruszania się wszystkich pionków 
  Zaimplementowane roszowanie
  Zaimplementowane bicie w przelocie
  Zaimplementowane związania
  Zaimplementowane sytuacja szachowa
  Kończenie rozgrywki przy możliwych rezultatach: poddanie partii, remis, pat, mat
  Obracanie szachownicy przy zmianie gracza
  Awans pionka przy dotarciu do końca szachownicy
  Ruch o dwa pola dla pionków bez wcześniejszego ruchu
  Wyświetlanie możliwych ruchów dla danego pionka
  Umożliwienie użytkownikowi wyboru czasu trwania partii oraz inkrementu (domyślnie 0)
  Wyświetlanie pozostałego czasu dla poszczególnych zawodników

  Przedstawienie zdobytego materiału dla poszczególnych graczy
  Zapisanie przebiegu partii do pliku


Lista klas:



class Engine:
   def __init__(self, chessboard):
      self.chessboard = chessboard
      self.current_player = 0

   def reset_figures_available_moves(chessboard):
       pass

class Chessboard:
   def __init__(self):
       self.board = [[0 for _ in range(8 + 1)] for _ in range(8 + 1)]

   def print_board(self):
       pass



class Figure():
   def __init__(self, board, color, piece, position):
       self.board = board
       self.piece = piece
       self.color = color
       self.position = position
       self.alive = True

   def move(self):
       pass


class Pawn(Figure):
   def __init__(self, second_row, board, color, piece, position):
       self.second_row = True
       Figure.__init__(self, board, color, piece, position)

   def promotion(self):
       pass




class Knight(Figure):
   def __init__(self, board, color, piece, position):
       Figure.__init__(self, board, color, piece, position)


class Bishop(Figure):
   def __init__(self, board, color, piece, position):
       Figure.__init__(self, board, color, piece, position)


class Rook(Figure):
   def __init__(self, board, color, piece, position):
       Figure.__init__(self, board, color, piece, position)


class Queen(Figure):
   def __init__(self, board, color, piece, position):
       Figure.__init__(self, board, color, piece, position)


class King(Figure):
  def __init__(self, right_to_castling, board, color, piece, position):
      self.right_to_castling = True
      self.is_checked = False
      Figure.__init__(self, board, color, piece, position)














