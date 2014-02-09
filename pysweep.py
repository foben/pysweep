#!/usr/bin/env python
"""
Welcome to PySweep
===================
A command line Minesweeper clone written in Python

Starting:
Usage: python pysweep.py height width mines
E.g.   python pysweep.py 10 10 5

Playing:
type "y, x" to clear a field (there should be no mine :) )
type "y, x," (trailing comma) to flag a field as mined
flag same field again to remove flag
type "solve" to check your solution
"""

import os, sys
import random
from datetime import datetime

__author__  = "Felix Obenauer"
__version__ = "1.0"

print __doc__

tf  = "  %s  "
tfr = " %02d  "

class Field():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False 
        self.revealed = False
        self.surr_mines = -1
        self.is_flagged = False

    def print_field(self):
        if self.is_flagged:
            return tf % "X"
        if not self.revealed:
            return tf % "?"
        else:
            if self.is_mine: return tf % "M"
            else:            return tf % self.surr_mines if self.surr_mines > 0 else tf % " "

    def __repr__(self):
        return "|%s,%s|" % (self.x, self.y)

class Board():
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [ [Field(i, j) for i in range(self.rows) ] for j in range(self.cols) ]
        self.place_mines()
        self.flagged = 0
        self.start = datetime.now()

    def reveal_board(self):
        for c in range(self.cols):
            for r in range(self.rows):
                self.board[c][r].surr_mines = self.get_surr_mines(c, r)
                self.board[c][r].revealed = True

    def place_mines(self):
        for i in range(self.mines):
            while True:
                rc = random.randint(0, self.cols - 1)
                rr = random.randint(0, self.rows - 1)
                if(not self.board[rc][rr].is_mine):
                    self.board[rc][rr].is_mine = True
                    break

    def get_elapsed(self):
        return (datetime.now() - self.start).total_seconds()

    def print_board(self):
        timestr = "Elapsed:  %f seconds" % self.get_elapsed()
	print "%d Mines total,   %d flagged, %d remaining!              %s\n"\
        % (self.mines, self.flagged, self.mines - self.flagged, timestr)
        firstrow = "     | "
        secrow   = "-----|-"
        for c in range(self.cols):
            firstrow += tfr % c
            secrow   += "-----"
        firstrow += " |"
        secrow += "-------"
        print firstrow
        print secrow
        for r in range(self.rows):
            row = " %02d  | " % r
            for c in range(self.cols):
                row += self.board[c][r].print_field()
            row += " |  %02d" % r
            print row
        print secrow
        print firstrow

    def flag(self, c, r):
        self.flagged += 1
        self.board[c][r].is_flagged = True

    def check_mine(self, c, r):
        if self.board[c][r].is_mine:
            return True
        surr_mines = self.get_surr_mines(c, r)
        self.board[c][r].surr_mines =surr_mines
        self.board[c][r].revealed = True
        if surr_mines == 0:
            for co in range(-1,2):
                for ro in range(-1,2):
                    tc = c + co
                    tr = r + ro
                    if tc < 0: continue
                    if tr < 0: continue
                    if tc >= self.cols: continue
                    if tr >= self.rows: continue
                    if tc == c and tr == r: continue
                    if self.board[tc][tr].revealed == True: continue
                    self.check_mine(tc, tr)
        
        return False

    def get_surr_mines(self, c, r):
        if self.board[c][r].is_mine:
            return 0
        mines = 0
        for co in range(-1,2):
            for ro in range(-1,2):
                tc = c + co
                tr = r + ro
                if tc < 0: continue
                if tr < 0: continue
                if tc >= self.cols: continue
                if tr >= self.rows: continue
                if tc == c and tr == r: continue
                if self.board[tc][tr].is_mine: mines += 1
        return mines

    def solve(self):
        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[c][r].is_mine and not self.board[c][r].is_flagged:
                    return False
                if not self.board[c][r].is_mine and self.board[c][r].is_flagged:
                    return False
        return True


def main():
    try:
        if len(sys.argv) != 4:
            raise ValueError()
        rows =  int(sys.argv[1])
        cols =  int(sys.argv[2])
        mines = int(sys.argv[3])
    except ValueError:
        print "Please specify board height, width and number of mines!"
        sys.exit()
    board = Board(rows, cols, mines)
    message = None
    while True:
        print "\n\n"
        board.print_board()
        if message:
            print message
            message = None
        input = raw_input("Enter Coordinates: ")
        seconds = board.get_elapsed()
        if input == "solve":
            if board.solve():
                print "YOU WIN!!!"
                print "It took you %f seconds" % seconds

            else:
                print "BOOOOOOOOOOOOM\nYOU LOST IN %f SECONDS!!!!" % seconds
            break
        coord = input.split(",")
        try:   
            if len(coord) != 2 and len(coord) != 3:
                raise ValueError()
            tr = int(coord[0])
            tc = int(coord[1])
        except ValueError:
            message = "Not a valid input, try again!"
            continue

        if len(coord) == 3:
            board.flag(tc, tr)
            continue
        if board.check_mine(tc, tr):
            print "BOOOOOOOOOOOOM\nYOU LOST IN %f SECONDS!!!!" % seconds
            break
        else:
            board.get_surr_mines(tc, tr)

main()
