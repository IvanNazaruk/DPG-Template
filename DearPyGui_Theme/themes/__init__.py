from enum import Enum

from . import blackdevil
from . import cherry
from . import classic
from . import classic_steam
from . import comfy
from . import darcula
from . import dark
from . import dark_ruda
from . import deep_dark
from . import discord_dark
from . import enemymouse
from . import gold
from . import green_font
from . import ledsynthmaster
from . import light
from . import material_flat
from . import microsoft
from . import photoshop
from . import red_font
from . import rounded_visual_studio
from . import soft_cherry
from . import sonic_riders
from . import unreal
from . import visual_studio


class THEME(Enum):
    CLASSIC = classic
    LIGHT = light
    DARK = dark
    CHERRY = cherry
    DARCULA = darcula
    PHOTOSHOP = photoshop
    UNREAL = unreal
    GOLD = gold
    VISUAL_STUDIO = visual_studio
    GREEN_FONT = green_font
    RED_FONT = red_font
    DEEP_DARK = deep_dark
    SONIC_RIDERS = sonic_riders
    CLASSIC_STEAM = classic_steam
    DARK_RUDA = dark_ruda
    MICROSOFT = microsoft
    SOFT_CHERRY = soft_cherry
    LEDSYNTHMASTER = ledsynthmaster
    ENEMYMOUSE = enemymouse
    MATERIAL_FLAT = material_flat
    DISCORD_DARK = discord_dark
    BLACKDEVIL = blackdevil
    ROUNDED_VISUAL_STUDIO = rounded_visual_studio
    COMFY = comfy
