# -*- coding: utf-8 -*-
"""生成任务一硬件接线示意图（STM32F103C8T6 + CH340 模块 + ST-Link）"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"F:\Fundamentals_of_Embedded_Systems\实验2-串口通信实验\images\15-硬件-STM32与模块接线示意图.png"
W, H = 1560, 980

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

CANDIDATES = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc",
              r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc"]


def font(size):
    for p in CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


F_TITLE, F_BOX, F_PIN, F_LAB, F_NOTE = font(40), font(28), font(23), font(22), font(23)
BOX_FILL, BOX_LINE = "#EAF2FB", "#2F6FB0"
BOARD_FILL, BOARD_LINE = "#F1F8EA", "#5B8C3E"
TXT, SUB = "#111827", "#37474F"


def tw(s, f):
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    return x1 - x0, y1 - y0, x0, y0


def center(cx, cy, s, f, fill=TXT):
    w, h, ox, oy = tw(s, f)
    d.text((cx - w / 2 - ox, cy - h / 2 - oy), s, font=f, fill=fill)


def box(x0, y0, x1, y1, title, fill=BOX_FILL, outline=BOX_LINE, title_cy=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=fill, outline=outline, width=3)
    lines = title.split("\n")
    lh = F_BOX.size + 12
    cy = title_cy if title_cy is not None else ((y0 + y1) / 2 - (len(lines) - 1) * lh / 2)
    for ln in lines:
        center((x0 + x1) / 2, cy, ln, F_BOX)
        cy += lh


def line(p1, p2, color=SUB, width=4):
    d.line([p1, p2], fill=color, width=width)


def arrow(p1, p2, color=SUB, width=4):
    line(p1, p2, color, width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L, Wd = 16, 8
    bx, by = p2[0] - L * math.cos(ang), p2[1] - L * math.sin(ang)
    d.polygon([p2, (bx - Wd * math.sin(ang), by + Wd * math.cos(ang)),
               (bx + Wd * math.sin(ang), by - Wd * math.cos(ang))], fill=color)


def label_on(cx, cy, s, f=F_LAB, color=TXT):
    w, h, ox, oy = tw(s, f)
    d.rectangle([cx - w / 2 - 7, cy - h / 2 - 5, cx + w / 2 + 7, cy + h / 2 + 5], fill="white")
    d.text((cx - w / 2 - ox, cy - h / 2 - oy), s, font=f, fill=color)


center(W / 2, 52, "任务一  硬件接线示意图", F_TITLE)

# 三个主要器件
box(70, 350, 330, 570, "上位机 PC\n(Win11 + 串口助手)")
box(450, 110, 760, 270, "ST-Link V2")
box(450, 560, 760, 830, "USB/TTL 模块\n(CH340)", title_cy=596)
box(1020, 110, 1470, 830, "STM32F103C8T6\n(Blue Pill)", fill=BOARD_FILL, outline=BOARD_LINE)

Y_SER = [650, 693, 736, 779]   # 串口四根线所在高度

# 模块引脚（名字写在盒内右侧）
for (name, col), y in zip([("TXD", "#C0392B"), ("RXD", "#1E8449"),
                           ("GND", SUB), ("VCC", "#D32F2F")], Y_SER):
    d.text((742, y), name, font=F_PIN, fill=col, anchor="rm")
    line((760, y), (768, y), col, 3)

# 板子引脚（名字写在盒内左侧）
for (name, col), y in zip([("PA13 / SWDIO", "#E67E22"), ("PA14 / SWCLK", "#E67E22"),
                           ("PA10 / USART1_RX", "#C0392B"), ("PA9 / USART1_TX", "#1E8449"),
                           ("GND", SUB), ("5V / 3V3（不接）", "#D32F2F")],
                          [190, 240] + Y_SER):
    line((1000, y), (1020, y), col, 3)
    d.text((1042, y), name, font=F_PIN, fill=col, anchor="lm")

# 下载线（USB）
arrow((330, 420), (450, 190), "#8E44AD")
label_on(390, 292, "USB", color="#8E44AD")
arrow((330, 500), (450, 640), "#8E44AD")
label_on(388, 566, "USB", color="#8E44AD")

# SWD 调试线
arrow((1000, 190), (760, 190), "#E67E22")
label_on(880, 190, "SWDIO", color="#E67E22")
arrow((1000, 240), (760, 240), "#E67E22")
label_on(880, 240, "SWCLK", color="#E67E22")

# 串口连线（同一行直连，用文字标注交叉关系）
arrow((768, Y_SER[0]), (1000, Y_SER[0]), "#C0392B")
label_on(884, Y_SER[0], "模块 TXD → PA10 (RX)", color="#C0392B")
arrow((1000, Y_SER[1]), (768, Y_SER[1]), "#1E8449")
label_on(884, Y_SER[1], "模块 RXD ← PA9 (TX)", color="#1E8449")
line((768, Y_SER[2]), (1000, Y_SER[2]), SUB)
label_on(884, Y_SER[2], "GND — GND", color=SUB)

# VCC 不接
line((768, Y_SER[3]), (880, Y_SER[3]), "#9E9E9E", 3)
line((872, Y_SER[3] - 8), (888, Y_SER[3] + 8), "#D32F2F", 4)
line((872, Y_SER[3] + 8), (888, Y_SER[3] - 8), "#D32F2F", 4)
d.text((900, Y_SER[3]), "VCC 不接", font=F_PIN, fill="#D32F2F", anchor="lm")

# 说明
d.text((70, 875), "说明：① 串口线必须交叉连接——模块 TXD 接 STM32 的 PA10(USART1_RX)，模块 RXD 接 PA9(USART1_TX)；",
       font=F_NOTE, fill=SUB)
d.text((108, 915), "② GND 必须相连，为双方电平提供公共的 0 V 参考；③ 模块由 USB 供电，VCC 不接。",
       font=F_NOTE, fill=SUB)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT)
print("saved:", img.size)
