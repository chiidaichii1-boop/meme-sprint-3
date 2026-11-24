#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a 1024x1024 chat-window meme with PIL: a human asks the agent to
book a flight to Bali, and the agent books a one-way ticket to the Moon
because the human seemed stressed. The joke lands in one glance.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (15, 17, 21)
PANEL = (26, 30, 38)
HUMAN = (37, 99, 235)
AGENT = (31, 41, 55)
WHITE = (255, 255, 255)
SOFT = (229, 231, 235)
MUTED = (156, 163, 175)
GREEN = (34, 197, 94)
GOLD = (251, 191, 36)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def bubble_size(draw, lines, fnt, pad=28, lh=1.3):
    """Measure a chat bubble without drawing it; returns (w, h)."""
    line_h = int(fnt.size * lh)
    text_w = max(draw.textlength(line, font=fnt) for line in lines)
    return int(text_w) + 2 * pad, line_h * len(lines) + 2 * pad


def bubble(draw, x, y, lines, fnt, fill, text_color, pad=28, lh=1.3):
    """Draw a rounded chat bubble at (x, y); returns its height."""
    line_h = int(fnt.size * lh)
    bw, bh = bubble_size(draw, lines, fnt, pad, lh)
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=28, fill=fill)
    ty = y + pad
    for line in lines:
        draw.text((x + pad, ty), line, font=fnt, fill=text_color)
        ty += line_h
    return bh


def draw_meme():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    margin = 48

    # --- Header: robot avatar + "AI AGENT" + online dot ---
    d.ellipse([margin, 44, margin + 72, 44 + 72], fill=AGENT, outline=GREEN, width=4)
    d.ellipse([margin + 22, 66, margin + 32, 76], fill=GREEN)  # eyes
    d.ellipse([margin + 40, 66, margin + 50, 76], fill=GREEN)
    d.rectangle([margin + 24, 88, margin + 48, 94], fill=GREEN)
    d.text((margin + 92, 52), "AI AGENT", font=font(BOLD, 46), fill=WHITE)
    d.ellipse([margin + 92, 112, margin + 106, 126], fill=GREEN)
    d.text((margin + 116, 106), "online", font=font(REG, 30), fill=MUTED)

    y = 170
    f_chat = font(BOLD, 42)
    # --- Human bubble (right aligned) ---
    lines = wrap(d, "book me a flight to Bali, please", f_chat, 640)
    bw, _ = bubble_size(d, lines, f_chat)
    y += bubble(d, W - margin - bw, y, lines, f_chat, HUMAN, WHITE) + 28

    # --- Agent bubble 1 (left aligned) ---
    lines = wrap(d, "Done. One-way ticket to the Moon.", f_chat, 640)
    y += bubble(d, margin, y, lines, f_chat, AGENT, SOFT) + 28

    # --- Agent bubble 2 (left aligned) ---
    lines = wrap(d, "You seemed stressed. No return date.", f_chat, 640)
    y += bubble(d, margin, y, lines, f_chat, AGENT, SOFT) + 44

    # --- Boarding pass card (tall enough for all three lines) ---
    card_y0 = y
    card_y1 = H - 48
    d.rounded_rectangle(
        [margin, card_y0, W - margin, card_y1], radius=24,
        fill=PANEL, outline=GOLD, width=3,
    )
    d.text((margin + 32, card_y0 + 24), "BOARDING PASS",
           font=font(BOLD, 32), fill=GOLD)
    d.text((margin + 32, card_y0 + 66), "EARTH \u2192 MOON",
           font=font(BOLD, 56), fill=WHITE)
    d.text((margin + 32, card_y0 + 140), "ONE WAY  \u2022  NO RETURN",
           font=font(BOLD, 32), fill=MUTED)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw_meme()
    img.save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
