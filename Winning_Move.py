def Horcheck(ar,chip,cnt=[0,0]):
    for y in range(len(ar)):
        for x in range(len(ar[y])-3):
            flag = 0
            for k in range(4):
                if ar[y][x+k] == chip:
                    flag += 1
            if flag == 4:
                cnt[chip] += 1
                return True

def Vercheck(ar,chip,cnt=[0,0]):
    for x in range(len(ar[0])):
        for y in range(len(ar)-3):
            flag = 0
            for k in range(4):
                if ar[y+k][x] == chip:
                    flag += 1
            if flag == 4:
                cnt[chip] += 1
                return True

def Diag1check(ar,chip,cnt=[0,0]):
    for y in range(len(ar)-3):
        for x in range(3, len(ar[y])):
            flag = 0
            for k in range(4):
                if ar[y+k][x-k] == chip:
                    flag += 1
            if flag == 4:
                cnt[chip] += 1
                return True

def Diag2check(ar,chip,cnt=[0,0]):
    for y in range(len(ar)-3):
        for x in range(len(ar[y])-3):
            flag = 0
            for k in range(4):
                if ar[y+k][x+k] == chip:
                    flag += 1
            if flag == 4:
                cnt[chip] += 1
                return True

def winning_move(board, piece):
    return Horcheck(board, piece) or Vercheck(board, piece) or Diag1check(board, piece) or Diag2check(board, piece)