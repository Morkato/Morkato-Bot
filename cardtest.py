from objects.types.player import PlayerBreed

from PIL import ImageDraw, ImageFont, Image

from easy_pil import Editor, Canvas

from numerize.numerize import numerize as num_fmt

from math import sqrt, pow

import numpy as np

BIG_SIZE = 4
CARD_MARGIN = 10

CARD_SIZE = np.array((642, 116), dtype=np.uint16)
CARD_INFO_SIZE = np.array(CARD_SIZE - CARD_MARGIN * 2, dtype=np.uint16)
AVATAR_SIZE =  np.array((76, 76), dtype=np.uint16)

MENU_SIZE = np.array((96, 32), dtype=np.uint16)
ICON_MENU_SIZE = np.array((32, 32), dtype=np.uint16)
BREED_ICON_SIZE = np.array((26, 26), dtype=np.uint16)

heart_icon = Editor("life.test.png")
ring_icon  = Editor("assets/ring.png")
human_icon = Editor("assets/human.png")
hybrid_icon = Editor("assets/hybrid.png")
oni_icon = Editor("assets/oni.png")
blood_icon = Editor("assets/blood.png")
breath_icon = Editor("assets/breath.png")

def circle_image(im: Image.Image) -> Image.Image:
  bigsize = (im.size[0] * 3, im.size[1] * 3)
  mask = Image.new('L', bigsize, 0)
  draw = ImageDraw.Draw(mask)

  draw.ellipse((0, 0) + bigsize, 255)
  mask = mask.resize(im.size, Image.ADAPTIVE)

  im.putalpha(mask)

  return im

def distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
  return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))

bigroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', 26)
mediumroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', 12)
smallroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', 10)

bigbigroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', bigroboto.size * BIG_SIZE)
bigmediumroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', mediumroboto.size * BIG_SIZE)
bigsmallroboto = ImageFont.FreeTypeFont('assets/Roboto-Bold.ttf', smallroboto.size * BIG_SIZE)

avatar_width = 76
avatar_height = 76

def create_avatar(im: Image.Image | str | Editor | Canvas) -> Editor:
  avatar = Editor(im).resize(tuple(AVATAR_SIZE * 4))

  avatar = avatar.rounded_corners(distance((0, 0), avatar.image.size) * .03)

  return avatar

def create_menu(icon: Image.Image | str | Editor | Canvas, text: str) -> Editor:
  background = Editor(Canvas(tuple(MENU_SIZE * BIG_SIZE), '#2E382E'))
  icon = icon.resize((icon.image.width * BIG_SIZE, icon.image.height * BIG_SIZE))

  canvas_icon = Canvas(tuple(ICON_MENU_SIZE * BIG_SIZE), '#2f3e46')
  background_icon = Editor(canvas_icon)

  x_icon = (icon.image.width - background_icon.image.width) // 2
  y_icon = (icon.image.height - background_icon.image.height) // 2

  x_icon = x_icon if not x_icon < 0 else x_icon * -1
  y_icon = y_icon if not y_icon < 0 else y_icon * -1
  
  background_icon.paste(icon, (x_icon, y_icon))

  draw = ImageDraw.Draw(background.image)

  x_text = (icon.image.width + background.image.width - draw.textlength(text, bigmediumroboto)) / 2
  y_text = (background.image.height - bigmediumroboto.size) / 2

  background.text((x_text, y_text), text, bigmediumroboto, '#ffffff')

  background.paste(background_icon, (0, 0))

  background = background.rounded_corners(distance((0, 0), background.image.size) * .02)

  return background

def card_headers(*,
  global_name: str,
  breed: PlayerBreed,
  username: str,
  name: str,
  life: int,
  breath: int,
  blood: int,
  credibility: int,
  exp: int
) -> Editor:
  card_headers = Editor(Canvas(tuple(CARD_INFO_SIZE * BIG_SIZE), '#282a36'))
  avatar       = create_avatar("card_image.test.png")

  exp = num_fmt(exp)

  draw = ImageDraw.Draw(card_headers.image)

  x_global_name = card_headers.image.width - draw.textlength(global_name, bigsmallroboto) - (15 * BIG_SIZE)
  y_global_name = card_headers.image.height - bigsmallroboto.size - (5 * BIG_SIZE)

  card_headers.text((x_global_name, y_global_name), '~ %s' % global_name, bigsmallroboto, (243, 230, 255))

  x_name = avatar.image.width + BIG_SIZE * 20
  y_name = 10 * BIG_SIZE

  card_headers.text((x_name, y_name), name, bigbigroboto, '#ffffff')

  x_username = x_name
  y_username = y_name + bigbigroboto.size + 2

  card_headers.text((x_username, y_username), username, bigmediumroboto, '#ffffff')

  breed_icon = None

  if breed == 'HUMAN':
    breed_icon = human_icon

  elif breed == 'ONI':
    breed_icon = oni_icon

  elif breed == 'HYBRID':
    breed_icon = hybrid_icon
  
  else:
    raise Exception('Player breed invalid')
  
  breed_icon = breed_icon.resize(tuple(BREED_ICON_SIZE * BIG_SIZE))

  x_breed = card_headers.image.width - breed_icon.image.width - 5 * BIG_SIZE
  y_breed = y_name

  card_headers.paste(breed_icon, (x_breed, y_breed))

  # x_exp = card_headers.image.width - draw.textlength(exp, bigmediumroboto) - (5 * BIG_SIZE)
  # y_exp = y_name + bigmediumroboto.size

  # card_headers.text((x_exp, y_exp), exp, bigmediumroboto, '#ffffff')

  info_life = create_menu(heart_icon.resize((22, 22)), num_fmt(life))

  x_menu = x_name
  y_menu = card_headers.image.height - info_life.image.height - 10

  card_headers.paste(info_life, (x_menu, y_menu))

  x_menu += info_life.image.width + (2 * BIG_SIZE)

  if breed in [ 'HUMAN', 'HYBRID' ]:
    info_breath = create_menu(breath_icon.resize((20, 20)), num_fmt(breath))

    card_headers.paste(info_breath, (x_menu, y_menu))

    x_menu += info_breath.image.width + (2 * BIG_SIZE)
  
  if breed in [ 'ONI', 'HYBRID' ]:
    info_blood = create_menu(blood_icon.resize((20, 20)), num_fmt(blood))

    card_headers.paste(info_blood, (x_menu, y_menu))

    x_menu += info_blood.image.width + (2 * BIG_SIZE)

  info_credibility = create_menu(ring_icon.resize((20, 20)), num_fmt(credibility))
  
  card_headers.paste(info_credibility, (x_menu, y_menu))

  x_menu += info_credibility.image.width + (2 * BIG_SIZE)

  card_headers.paste(avatar, (10 * BIG_SIZE, 10 * BIG_SIZE))
  
  card_headers = card_headers.resize(tuple(CARD_INFO_SIZE))

  # card.paste(card_info, (10, 10))

  return card_headers

def card(*,
  global_name: str,
  breed: PlayerBreed,
  username: str,
  name: str,
  life: int,
  breath: int,
  blood: int,
  credibility: int,
  exp: int
) -> Editor:
  headers = card_headers(
    global_name=global_name,
    breed=breed,
    username=username,
    name=name,
    life=life,
    breath=breath,
    blood=blood,
    credibility=credibility,
    exp=exp
  )

  height = headers.image.height + 20

  if appearance:
    height += appearance.image.height + 20
  
  canvas = Canvas((headers.image.width + 20, height), '#44475a')
  card = Editor(canvas)

  headers = headers.rounded_corners(distance((0, 0), headers.image.size) * .01)
  
  card.paste(headers, (10, 10))

  if not appearance:
    return card

  canvas = Canvas((appearance.image.width + 20, height), '#44475a')
  photo = Editor(canvas)

  appearance = appearance.rounded_corners(distance((0, 0), appearance.image.size) * .01)

  photo.paste(appearance, (10, 10))

  card.paste(photo, (10, headers.image.height + 10))

  return card