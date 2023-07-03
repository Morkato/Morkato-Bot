from typing import Literal

from PIL import Image, ImageDraw
from copy import deepcopy

class Snake:
  def __init__(self, *, pos: tuple[int, int] = (200, 200), size: int = 10, direction: Literal["UP", "DOWN", "LEFT", "RIGHT"] = "UP", initial_cont_body: int = 5) -> None:
    self.size = size
    self.direction = direction

    self.body: list[tuple[int, int]] = [pos,] + [ (pos[0]+size*i, pos[1]) for i in range(initial_cont_body) ]
  
  def render(self, img: Image.Image) -> None:
    draw = ImageDraw.ImageDraw(img)

    for x, y in self.body:
      draw.rectangle((x, y, x+self.size, y+self.size), (255, 255, 255))
  
  def next(self) -> None:
    for i in range(len(self.body)-1, 0, -1):
      self.body[i] = deepcopy(self.body[i-1])
    
    if self.direction == 'UP':
      self.body[0] = ( self.body[0][0], self.body[0][1]-self.size )
    
    elif self.direction == 'DOWN':
      self.body[0] = ( self.body[0][0], self.body[0][1]+self.size )
    
    elif self.direction == 'LEFT':
      self.body[0] = ( self.body[0][0]-self.size, self.body[0][1] )

    elif self.direction == 'RIGHT':
      self.body[0] = ( self.body[0][0]+self.size, self.body[0][1] )


def get_background():
  return Image.new("RGB", (600, 400), 0)