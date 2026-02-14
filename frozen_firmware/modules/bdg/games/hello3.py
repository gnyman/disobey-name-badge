import asyncio
import json
import math
import os
import hardware_setup as hardware_setup
from neopixel import NeoPixel
from hardware_setup import LED_ACTIVATE_PIN, LED_PIN

from gui.core.ugui import Screen, ssd
from gui.core.colors import BLACK, WHITE
from gui.core.writer import CWriter
from gui.fonts import font10

from bdg.asyncbutton import ButtonEvents, ButAct
from bdg.bleds import clear_leds
from bdg.widgets.hidden_active_widget import HiddenActiveWidget

BUILD_TIME = "2026-02-14"
CONFIG_FILE = "hello2_badge.json"
LED_COUNT = 10

EFFECTS = ["ZOOM", "SINE", "SCROLL", "PLASMA"]

THEMES = [
    {
        "name": "MATRIX",
        "bg": ssd.rgb(0, 0, 0),
        "colors": [ssd.rgb(30, 255, 80), ssd.rgb(0, 180, 30), ssd.rgb(120, 255, 160)],
    },
    {
        "name": "CYBER",
        "bg": ssd.rgb(0, 0, 0),
        "colors": [ssd.rgb(0, 240, 255), ssd.rgb(255, 0, 255), ssd.rgb(120, 180, 255)],
    },
    {
        "name": "FIRE",
        "bg": ssd.rgb(0, 0, 0),
        "colors": [ssd.rgb(255, 60, 20), ssd.rgb(255, 150, 0), ssd.rgb(255, 220, 120)],
    },
    {
        "name": "VAPOR",
        "bg": ssd.rgb(22, 0, 34),
        "colors": [ssd.rgb(255, 120, 220), ssd.rgb(160, 120, 255), ssd.rgb(120, 220, 255)],
    },
    {
        "name": "RETRO",
        "bg": ssd.rgb(0, 26, 12),
        "colors": [ssd.rgb(0, 255, 100), ssd.rgb(255, 220, 0), ssd.rgb(255, 80, 180)],
    },
]

LED_COLORS = [
    {"name": "RED", "rgb": (255, 0, 0)},
    {"name": "GREEN", "rgb": (0, 255, 0)},
    {"name": "BLUE", "rgb": (0, 0, 255)},
    {"name": "CYAN", "rgb": (0, 255, 255)},
    {"name": "MAGENTA", "rgb": (255, 0, 255)},
    {"name": "YELLOW", "rgb": (255, 255, 0)},
    {"name": "WHITE", "rgb": (255, 255, 255)},
    {"name": "ORANGE", "rgb": (255, 128, 0)},
    {"name": "PINK", "rgb": (255, 20, 147)},
    {"name": "PURPLE", "rgb": (150, 0, 255)},
]

GLYPHS = {
    " ": ("     ", "     ", "     ", "     ", "     "),
    "!": ("  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "?": (" ### ", "#   #", "  ## ", "     ", "  #  "),
    "-": ("     ", "     ", " ### ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "  #  "),
    "@": (" ### ", "# # #", "# ###", "#    ", " ### "),
    "#": (" # # ", "#####", " # # ", "#####", " # # "),
    "_": ("     ", "     ", "     ", "     ", "#####"),
    "/": ("    #", "   # ", "  #  ", " #   ", "#    "),
    "+": ("  #  ", "  #  ", "#####", "  #  ", "  #  "),
    ":": ("     ", "  #  ", "     ", "  #  ", "     "),
    ";": ("     ", "  #  ", "     ", "  #  ", " #   "),
    ",": ("     ", "     ", "     ", "  #  ", " #   "),
    "(": ("   # ", "  #  ", "  #  ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "  #  ", "  #  ", " #   "),
    "[": (" ### ", " #   ", " #   ", " #   ", " ### "),
    "]": (" ### ", "   # ", "   # ", "   # ", " ### "),
    "0": (" ### ", "#   #", "#   #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "   # ", "  #  ", "#####"),
    "3": ("#### ", "    #", " ### ", "    #", "#### "),
    "4": ("#  # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "#### "),
    "6": (" ### ", "#    ", "#### ", "#   #", " ### "),
    "7": ("#####", "   # ", "  #  ", " #   ", " #   "),
    "8": (" ### ", "#   #", " ### ", "#   #", " ### "),
    "9": (" ### ", "#   #", " ####", "    #", " ### "),
    "A": (" ### ", "#   #", "#####", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#### ", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#### ", "#    ", "#####"),
    "F": ("#####", "#    ", "#### ", "#    ", "#    "),
    "G": (" ####", "#    ", "#  ##", "#   #", " ####"),
    "H": ("#   #", "#   #", "#####", "#   #", "#   #"),
    "I": ("#####", "  #  ", "  #  ", "  #  ", "#####"),
    "J": ("#####", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "###  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "#  ##", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#### ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#  ##", " ####"),
    "R": ("#### ", "#   #", "#### ", "#  # ", "#   #"),
    "S": (" ####", "#    ", " ### ", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "# # #", "## ##", "#   #"),
    "X": ("#   #", " # # ", "  #  ", " # # ", "#   #"),
    "Y": ("#   #", " # # ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "   # ", "  #  ", " #   ", "#####"),
}


class Hello3Screen(Screen):
    MODE_EDIT = 0
    MODE_DISPLAY = 1
    MAX_TEXT_LEN = 12
    CHARSET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?-.@#_/+:;,()[]"
    SCREEN_W = 320
    SCREEN_H = 170
    TEXT_TOP = 8
    TEXT_BOTTOM = 148
    TEXT_H = TEXT_BOTTOM - TEXT_TOP

    def __init__(self):
        super().__init__()
        self._hidden_writer = CWriter(ssd, font10, WHITE, BLACK, verbose=False)
        self._hidden_widget = HiddenActiveWidget(self._hidden_writer)

        cfg = self._load_config()
        self.text = cfg.get("text", "HACKER")
        self.effect_idx = cfg.get("effect_idx", 0) % len(EFFECTS)
        self.theme_idx = cfg.get("theme_idx", 0) % len(THEMES)
        self.led_idx = cfg.get("led_idx", 0) % len(LED_COLORS)

        self.char_idx = 0
        self.mode = self.MODE_DISPLAY
        self.running = True
        self.tick = 0
        self.needs_redraw = True
        self._force_full_redraw = True

        self.led_power = LED_ACTIVATE_PIN
        self.led_power.value(1)
        self.np = NeoPixel(LED_PIN, LED_COUNT)

        events = ButtonEvents.get_event_subset(
            [
                ("btn_u", ButAct.ACT_PRESS),
                ("btn_d", ButAct.ACT_PRESS),
                ("btn_l", ButAct.ACT_PRESS),
                ("btn_r", ButAct.ACT_PRESS),
                ("btn_a", ButAct.ACT_PRESS),
                ("btn_b", ButAct.ACT_PRESS),
                ("btn_b", ButAct.ACT_LONG),
                ("btn_select", ButAct.ACT_PRESS),
                ("btn_start", ButAct.ACT_PRESS),
            ]
        )
        self.be = ButtonEvents(events)

    def _load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def _save_config(self):
        try:
            data = {
                "text": self.text,
                "effect_idx": self.effect_idx,
                "theme_idx": self.theme_idx,
                "led_idx": self.led_idx,
            }
            tmp = CONFIG_FILE + ".tmp"
            with open(tmp, "w") as f:
                json.dump(data, f)
            os.rename(tmp, CONFIG_FILE)
        except Exception:
            pass

    def after_open(self):
        self.reg_task(self._button_loop(), True)
        self.reg_task(self._render_loop(), True)
        self.reg_task(self._led_loop(), True)

    def on_hide(self):
        self.running = False
        self._save_config()
        clear_leds(self.np)
        self.led_power.value(0)

    async def _button_loop(self):
        async for btn, ev in self.be.get_btn_events():
            if not self.running:
                break
            if btn == "btn_b" and ev == ButAct.ACT_LONG:
                Screen.back()
                continue
            if ev != ButAct.ACT_PRESS:
                continue

            if self.mode == self.MODE_EDIT:
                self._handle_edit(btn)
            else:
                self._handle_display(btn)

            self.needs_redraw = True

    def _handle_edit(self, btn):
        if btn == "btn_u":
            self.char_idx = (self.char_idx - 1) % len(self.CHARSET)
        elif btn == "btn_d":
            self.char_idx = (self.char_idx + 1) % len(self.CHARSET)
        elif btn == "btn_a":
            if len(self.text) < self.MAX_TEXT_LEN:
                self.text += self.CHARSET[self.char_idx]
                self._save_config()
        elif btn == "btn_b":
            if self.text:
                self.text = self.text[:-1]
                self._save_config()
        elif btn == "btn_start":
            self.text = ""
            self._save_config()
        elif btn == "btn_select":
            self.mode = self.MODE_DISPLAY
            self._force_full_redraw = True

    def _handle_display(self, btn):
        if btn == "btn_l":
            self.effect_idx = (self.effect_idx - 1) % len(EFFECTS)
            self._save_config()
        elif btn == "btn_r":
            self.effect_idx = (self.effect_idx + 1) % len(EFFECTS)
            self._save_config()
        elif btn == "btn_u":
            self.theme_idx = (self.theme_idx - 1) % len(THEMES)
            self._force_full_redraw = True
            self._save_config()
        elif btn == "btn_d":
            self.theme_idx = (self.theme_idx + 1) % len(THEMES)
            self._force_full_redraw = True
            self._save_config()
        elif btn == "btn_a":
            self.led_idx = (self.led_idx + 1) % len(LED_COLORS)
            self._save_config()
        elif btn == "btn_select":
            self.mode = self.MODE_EDIT
            self._force_full_redraw = True

    async def _render_loop(self):
        while self.running:
            effect = EFFECTS[self.effect_idx]
            animating = self.mode == self.MODE_DISPLAY and effect in ("SINE", "SCROLL", "PLASMA")

            if self.needs_redraw or animating:
                self._draw()
                self.needs_redraw = False
                if animating:
                    self.tick += 1

            await asyncio.sleep_ms(66)

    def _draw(self):
        theme = THEMES[self.theme_idx]
        if self._force_full_redraw:
            ssd.fill(theme["bg"])
            self._force_full_redraw = False
        else:
            if self.mode == self.MODE_EDIT:
                ssd.fill(theme["bg"])
            else:
                ssd.fill_rect(0, self.TEXT_TOP, self.SCREEN_W, self.TEXT_H, theme["bg"])

        if self.mode == self.MODE_EDIT:
            self._draw_edit(theme)
        else:
            self._draw_display(theme)
        ssd.show()

    def _draw_edit(self, theme):
        current = self.CHARSET[self.char_idx]
        text_view = self.text if self.text else "(empty)"

        ssd.text("NAME BADGE - EDIT", 8, 10, theme["colors"][0])
        ssd.text("BUILD {}".format(BUILD_TIME), 8, 24, theme["colors"][1])
        ssd.text("Text: {}".format(text_view), 8, 44, theme["colors"][2])
        ssd.text("Char: [{}]".format(current), 8, 60, theme["colors"][1])
        ssd.text("UP/DOWN: change char", 8, 84, theme["colors"][0])
        ssd.text("YELLOW: append  RED: delete", 8, 98, theme["colors"][0])
        ssd.text("GREEN: clear", 8, 112, theme["colors"][0])
        ssd.text("BLUE: display", 8, 126, theme["colors"][0])
        ssd.text("Hold RED: exit menu", 8, 140, theme["colors"][0])
        ssd.text("author @gnyman / nyman.re", 8, 154, theme["colors"][1])

    def _draw_display(self, theme):
        text = (self.text or "HACKER").upper()
        effect = EFFECTS[self.effect_idx]
        color = theme["colors"][0]

        if effect == "SINE":
            y_offset = int(math.sin(self.tick * 0.2) * 12)
            self._draw_big_text(text, color, y_offset=y_offset)
        elif effect == "SCROLL":
            self._draw_scroll_text(text, color)
        elif effect == "PLASMA":
            color = theme["colors"][(self.tick // 3) % len(theme["colors"])]
            self._draw_big_text(text, color, y_offset=0)
        else:
            self._draw_big_text(text, color, y_offset=0)

    def _draw_big_text(self, text, color, y_offset=0):
        scale = self._calc_scale(len(text))
        block_w = 5 * scale
        block_h = 5 * scale
        spacing = scale

        text_w = len(text) * (block_w + spacing) - spacing if text else block_w
        start_x = (self.SCREEN_W - text_w) // 2
        start_y = self.TEXT_TOP + (self.TEXT_H - block_h) // 2 + y_offset

        self._draw_glyphs(text, color, start_x, start_y, scale)

    def _draw_scroll_text(self, text, color):
        scale = self._calc_scale(len(text))
        block_w = 5 * scale
        spacing = scale
        text_w = len(text) * (block_w + spacing) - spacing if text else block_w
        period = text_w + self.SCREEN_W + scale * 2
        x = self.SCREEN_W - ((self.tick * (scale // 3 + 2)) % period)
        y = self.TEXT_TOP + (self.TEXT_H - (5 * scale)) // 2

        self._draw_glyphs(text, color, x, y, scale)
        self._draw_glyphs(text, color, x + text_w + scale * 2, y, scale)

    def _calc_scale(self, text_len):
        chars = text_len if text_len > 0 else 1
        max_h = self.TEXT_H // 5
        max_w = (self.SCREEN_W - 12) // (chars * 6)
        scale = min(max_h, max_w)
        if scale < 3:
            return 3
        return scale

    def _draw_glyphs(self, text, color, start_x, start_y, scale):
        x = start_x
        for ch in text:
            glyph = GLYPHS.get(ch, GLYPHS["?"])
            self._draw_glyph(glyph, color, x, start_y, scale)
            x += 6 * scale

    def _draw_glyph(self, glyph, color, x0, y0, scale):
        for gy in range(5):
            row = glyph[gy]
            for gx in range(5):
                if row[gx] == "#":
                    px = x0 + gx * scale
                    py = y0 + gy * scale
                    x1 = px if px > 0 else 0
                    y1 = py if py > self.TEXT_TOP else self.TEXT_TOP
                    x2 = px + scale
                    y2 = py + scale
                    if x2 > self.SCREEN_W:
                        x2 = self.SCREEN_W
                    if y2 > self.TEXT_BOTTOM:
                        y2 = self.TEXT_BOTTOM
                    if x1 >= x2 or y1 >= y2:
                        continue
                    ssd.fill_rect(x1, y1, x2 - x1, y2 - y1, color)

    async def _led_loop(self):
        led_tick = 0
        while self.running:
            if self.mode == self.MODE_EDIT:
                self._apply_led_static()
            else:
                self._apply_led_rotate(led_tick)
                led_tick += 1
            self.np.write()
            await asyncio.sleep_ms(200)

    def _apply_led_static(self):
        r, g, b = LED_COLORS[self.led_idx]["rgb"]
        static = (int(r * 0.05), int(g * 0.05), int(b * 0.05))
        for i in range(self.np.n):
            self.np[i] = static

    def _apply_led_rotate(self, led_tick):
        r, g, b = LED_COLORS[self.led_idx]["rgb"]
        count = self.np.n
        lead = led_tick % count
        for i in range(count):
            distance = (lead - i) % count
            if distance == 0:
                bright = 0.5
            elif distance <= 4:
                bright = (5 - distance) * 0.09
            else:
                bright = 0.01
            self.np[i] = (int(r * bright), int(g * bright), int(b * bright))


def badge_game_config():
    return {
        "con_id": 8,
        "title": "Name Badge 3",
        "screen_class": Hello3Screen,
        "screen_args": (),
        "multiplayer": False,
        "description": "Editable name badge with big text effects and LED animations",
    }
