from asyncio.windows_events import NULL
import matplotlib.pyplot as plt 

from datetime import datetime
from math import *
 
class Graph:
   
    def __init__(self, width_ = 12, height_ = 7, int_x = True, int_y = True):
        plt.figure(figsize = (width_, height_))

        self.int_x = int_x
        self.int_y = int_y
        
    def __Int_axis(self, int_x, int_y):

        def Calc_axis_points(ax_min, ax_max):
            if ax_min < 0:
                ax_min = 0

            step = ceil((ax_max - ax_min) / 12)
            return range(floor(ax_min), ceil(ax_max) + 1, step)

        xmin, xmax, ymin, ymax = plt.axis()
        
        if int_x == True:
            plt.xticks(Calc_axis_points(xmin, xmax))
            plt.xlim([xmin, xmax])

        if int_y == True:
            plt.yticks(Calc_axis_points(ymin, ymax))
            plt.ylim([ymin, ymax])
            
    def __Create_title(self, filetype, end):
        name = filetype + str(datetime.now()).replace(":", "_")  +  \
                     end;

        return name;

    def Set_labels(self, label_ = "", x_label_ = "", y_label_ = ""):
         plt.suptitle(label_, fontsize = 20)
         plt.xlabel(x_label_, fontsize = 18)
         plt.ylabel(y_label_,fontsize =  18) 

    def Create_plot(self, X, Y, grid_ = 0.75, alpha_ = 0.4, color_ = "green", 
                                linewidth_ = 2):

        plt.plot(X, Y, alpha = alpha_, color = color_, linewidth = linewidth_, marker ='D', markersize = 3)
        plt.grid(alpha = grid_, linestyle = '--')
                
    def Save_figure(self, name_ = NULL):
        if name_ == NULL: 
            name_ =  self.__Create_title("pic ", ".jpg")
        
        self.__Int_axis(self.int_x, self.int_y)
        plt.savefig(name_)
        return name_
        




