import pcbnew
import os
import wx
from .fillet_rectangles_gui import RadiusInputDialog


def circularArrayRotation(a, k):
    new_arr = a[k%len(a):] + a[:k%len(a)]
    return new_arr

class FilletRectangles(RadiusInputDialog):
    def __init__(self, board, action):
        super(FilletRectangles, self).__init__(None)
        self.board = board
        self.action = action

    def add_line(self, start, end, layer=pcbnew.Edge_Cuts):

        segment = pcbnew.PCB_SHAPE(self.board)
        segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
        segment.SetStart(start)
        segment.SetEnd(end)
        segment.SetLayer(layer)
        segment.SetWidth(int(0.1 * pcbnew.IU_PER_MM))
        self.board.Add(segment)


    def add_line_arc(self, start, center, angle=90, layer=pcbnew.Edge_Cuts):
        arc = pcbnew.PCB_SHAPE(self.board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        arc.SetStart(start)
        arc.SetCenter(center)
        arc.SetArcAngleAndEnd(angle * 10, False)
        arc.SetLayer(layer)
        arc.SetWidth(int(0.1 * pcbnew.IU_PER_MM))
        self.board.Add(arc)

    def RadiusInputDialogOnClose( self, event ):
        self.EndModal(wx.ID_OK)

    def runScript( self, event ):
        radius = float(self.t1.GetLineText(0))

        number_of_selected_rectangles = 0
        for drw in self.board.GetDrawings():
            if(drw.IsSelected() and str(drw.SHAPE_T_asString()) == "S_RECT"):

                try:

                    number_of_selected_rectangles +=1
                    unorganized_rect_data = drw.GetRectCorners()
                    top_left_corner = unorganized_rect_data[0]
                    top_left_corner_index = 0

                    for i in range(len(unorganized_rect_data)):
                        if((unorganized_rect_data[i].x <= top_left_corner.x) and (unorganized_rect_data[i].y <= top_left_corner.y)):
                            top_left_corner = unorganized_rect_data[i]
                            top_left_corner_index = i
                    rectData = circularArrayRotation(unorganized_rect_data, top_left_corner_index)

                    radius_x_offset = pcbnew.wxPoint(radius * pcbnew.IU_PER_MM, 0)
                    radius_y_offset = pcbnew.wxPoint(0, radius * pcbnew.IU_PER_MM)
                    self.add_line(rectData[0] + radius_x_offset, rectData[1] - radius_x_offset) # Top left - Top right
                    self.add_line(rectData[1] + radius_y_offset, rectData[2] - radius_y_offset) # Top Right - bottom right
                    self.add_line(rectData[2] - radius_x_offset, rectData[3] + radius_x_offset) # bottom right - bottom left
                    self.add_line(rectData[3] - radius_y_offset, rectData[0] + radius_y_offset) # bottom left - top left
                    self.add_line_arc(rectData[0] + radius_y_offset, rectData[0] + radius_y_offset + radius_x_offset, angle=90) # top left
                    self.add_line_arc(rectData[1] - radius_x_offset, rectData[1] - radius_x_offset + radius_y_offset, angle=90) # top right
                    self.add_line_arc(rectData[2] - radius_y_offset, rectData[2] - radius_y_offset - radius_x_offset, angle=90) # bottom right
                    self.add_line_arc(rectData[3] + radius_x_offset, rectData[3] + radius_x_offset - radius_y_offset, angle=90) # bottom left
                    self.board.RemoveNative(drw)
                    self.EndModal(wx.ID_OK)
                except Exception as e:
                    wx.MessageBox(str(e), 'Info',  wx.OK | wx.ICON_INFORMATION)
        if number_of_selected_rectangles == 0:
            wx.MessageBox("Please select a rectangle", 'Info',  wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)


class FilletRectanglesAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Fillet Rectangles"
        self.category = "fillet tools"
        self.description = "Select a rectangle and run the plugin to fillet the rectangle"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # Optional




    def Run(self):
        # The entry function of the plugin that is executed on user action
        board = pcbnew.GetBoard()
        rt = FilletRectangles(board, self)
        rt.ShowModal()
        pcbnew.UpdateUserInterface()
