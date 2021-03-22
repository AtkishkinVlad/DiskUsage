class ProgressBar:
    def __init__(self, totalItem):
        self.currentItem = 0
        self.totalItem = totalItem if totalItem != 0 else 1
        self.totalCharacterInLine = 50

    def nextState(self):
        self.currentItem = min(self.currentItem + 1, self.totalItem)
        coloredChars = (self.currentItem * self.totalCharacterInLine) // self.totalItem
        print("\r[" + '▮' * coloredChars + '_' * (self.totalCharacterInLine - coloredChars) + f"] : {self.currentItem * 100 // self.totalItem} percents done", end='')

    def finish(self):
        print('')