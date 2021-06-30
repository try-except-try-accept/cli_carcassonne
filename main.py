from random import randint, shuffle
from copy import deepcopy

TILE_SIZE = 5
TIlE_MAP_WIDTH = 5
TILE_MAP_HEIGHT = 3

symbols = [chr(i) for i in range(250, 500)]
shuffle(symbols)

MENU = """Rotate the tile
Place the tile
Change board""".split("\n")

zoom = False

BOARD = [[]]

def validate_move(x, y, tile):
     return True
     
def get_num(x):
     try:
          return int(x)
     except:
          return 0

def load_tiles():
     with open("tiles.csv") as f:
          lines = f.read()

     lines = lines.split("\n")

     tiles = [[]]
     for y, line in enumerate(lines[1:]):
          if y % 5 == 0 and y != 0:
               tiles.append([])

          tiles[-1].append(list(map(get_num, line.split(","))))

     return tiles

def get_symbol(tile):
     return int(sum([sum(row) for row in tile]) / TILE_SIZE ** TILE_SIZE)

def rotate(tile):
     # push hi push hi push lo
     # 00 04 44 40
     # 0,0 -> 0,4 -> 4,4 -> 4,0

     # 1,1 -> 1,3 -> 3,3 -> 3,1

     # 11111   12345     0,0 -> 0,4     4,0 ->  0 0      1,1 -> 1, 3,  
     # 2   2   1   5     4,4 -> 4,0                      1,3 -> 3, 3
     # 3   3   1  45     2,2 -> 2,2
     # 4 4 4   1   5
     # 55555   12345
     
     new_tile = deepcopy(tile)
     for y in range(len(tile)):
          for x in range(len(tile[0])):
               coords = [x,y]
               low = min(coords)
               if x != y:
                    hi = max(coords)
               else:
                    hi = TILE_SIZE - 1 - low
                    
               #print(f"Moving {coords} to ",end = "")
               
               coords.pop(0)
               if x == y == hi:
                    coords.append(low)
               else:
                    coords.append(hi)
               
               #print(coords)
               a, b = coords
               new_tile[y][x] = tile[b][a]

               display_tile(new_tile)
                    
     return new_tile
               
          


def get_ref(board):
     cols = [chr(i) for i in range(65, 65+len(board[0]))]
     rows = [chr(i) for i in range(65, 65+len(board))]
     valid_refs = []
     for x in cols:
          for y in rows:
               valid_refs.append(x+y)

     print(valid_refs)
     ref = input("Enter grid reference of where you want to place the tile" ).upper()
     while ref not in valid_refs:
          ref = input("Invalid. Re-enter: ").upper()
          
     return ord(ref[0])-65, ord(ref[1])-65
             

def display_game(zoom, birds_eye, board):
     for pos in [0, -1]:
          if any([cell!=[] for cell in board[pos]]):
               birds_eye.insert(pos, [" "] * len(board[0]))
               board.insert(pos, [[]] * len(board[0]))
          
     if any(cell!=[] for cell in [row[0] for row in board]):
          [row.insert(0, " ") for row in birds_eye]
          [row.insert(0, []) for row in board]

     if any(cell!=[] for cell in [row[-1] for row in board]):
          [row.append(" ") for row in birds_eye]
          [row.append([]) for row in board]
     

     spacer = " "

     print("X", end=spacer)
     
     for i in range(0, len(board[0])):
          print(chr(65+i), end=spacer)

     print()

     if not zoom:

          for i, row in enumerate(birds_eye):
               print(chr(65+i), end=spacer)
               for tile in row:
                    print(tile, end=spacer)
               print()
          


def display_tile(t):
     for row in t:
          for cell in row:
               print(cell, end="")
          print()


     
def get_action():

     for i, action in enumerate(MENU):
          print(f"Press {i+1} to {action}")

     valid = [str(i) for i in range(1, len(MENU)+1)]

     x = input()
     while x not in valid:
          x = input("Invalid. Please re-enter")

     return x
     

tiles = load_tiles()

tiles_copy = list(tiles)
shuffle(tiles)


rows = randint(3, 7)
cols = randint(3, 7)
board = [[[] for y in range(rows)] for x in range(cols)]
birds_eye = [['' for cell in row] for row in board]

game_over = False
while not game_over:

     tile = tiles.pop(0)

     print("You picked a tile!")
     print()
     display_tile(tile)

     sym = symbols.pop(0)
     print("We'll also refer to this tile as '{}'".format(sym))

     move_valid = False

     while not move_valid:

          display_game(zoom, birds_eye, board)
          
          choice = get_action()

          if choice == "1":
               tile = rotate(tile)
               print("You rotated the tile!")
               display_tile(tile)
               continue
          elif choice == "2":
               zoom = not zoom
          else:
               x, y = get_ref(board)

          move_valid = validate_move(x, y, tile)

          if move_valid:
               birds_eye[y][x] = sym
               board[y][x] = tile

     

     

               
          
          
          
          
          

