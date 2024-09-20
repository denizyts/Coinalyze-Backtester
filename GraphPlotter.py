import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime as dt

def draw(wallet_value_list , name):

 
 plt.plot(wallet_value_list)
 plt.title(name)

 plt.show()
