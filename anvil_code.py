from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.server
import json



class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_1.text = "Run"
    self.label_5.text = "To search for a specific coordinate, run the program then type a 3-tuple (i.e. (0,0,0)) below and click enter. Note that this should be in (z,y,x) form."
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    x = self.text_box_1.text
    y= self.text_box_2.text
    corners = self.text_box_3.text
    validity,msg = anvil.server.call('validate_inputs',x ,y,
                                     corners = self.text_box_3.text)
    if(not validity): 
      self.label_3.text = msg
    else:
      dims = (float(x),float(y))
      solution,done_msg = anvil.server.call('main',dims,corners)
      self.label_3.text = done_msg
      self.label_4.text = solution
      fig,data,layout = anvil.server.call('plot',solution)
      self.plot_1.figure = fig
      self.plot_1.data = data
      self.plot_1.layout = layout

      

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_3_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_4_pressed_enter(self, **event_args):
    x = self.text_box_1.text
    y= self.text_box_2.text
    corners = self.text_box_3.text
    point_to_search = eval(self.text_box_4.text)
    dims = (float(x),float(y))
    solution,done_msg = anvil.server.call('main',dims,corners)
    point = anvil.server.call('point_getter',solution,point_to_search)
    if point is not 'n/a':
      self.label_6.text = f'The point at the given coordinate is {point}.'
      self.label_6.bold = True 
      self.label_6.align = "center"
      self.label_6.font_size = 20 

    else:
      self.label_6.text = f'The given point is not a valid coordinate for the given rectangle and dimensions.'      
      self.label_6.bold = True
      self.label_6.align = "center" 
      self.label_6.font_size = 20 




