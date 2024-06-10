# Auteur   : Küenzi Jean-Daniel
# Desc.    :
# Date     : 12.02.2019

class Solution():
    def __init__(self):
        self.individual = None
        self.generation = 0

    def __str__(self):
        return 'Generation #{:d} - {:s}'.format(self.generation, str(self.individual))