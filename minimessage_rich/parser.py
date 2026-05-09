import re
from typing import List, Tuple, Optional
from rich.text import Text
from rich.style import Style
from rich.color import Color, ColorTriplet

class MiniMessageParser:
    COLORS = {
        "black": "#000000", "dark_blue": "#0000aa", "dark_green": "#00aa00",
        "dark_aqua": "#00aaaa", "dark_red": "#aa0000", "dark_purple": "#aa00aa",
        "gold": "#ffaa00", "gray": "#aaaaaa", "dark_gray": "#555555",
        "blue": "#5555ff", "green": "#55ff55", "aqua": "#55ffff",
        "red": "#ff5555", "light_purple": "#ff55ff", "yellow": "#ffff55",
        "white": "#ffffff",
        "magenta": "#ff55ff", "purple": "#aa00aa", "cyan": "#55ffff",
        "dark_cyan": "#00aaaa", "light_gray": "#aaaaaa",
    }
    
    RAINBOW_COLORS = ["red", "gold", "yellow", "green", "aqua", "blue", "light_purple"]

    def __init__(self):
        self.tag_pattern = re.compile(r"<(/?[a-z0-9_:#\.\-]*(?::(?:'[^']*'|[^>]+))*)/?>")

    def _parse_tag_parts(self, tag_content: str) -> List[str]:
        parts = []
        current = []
        in_quotes = False
        for char in tag_content:
            if char == "'":
                in_quotes = not in_quotes
                current.append(char)
            elif char == ":" and not in_quotes:
                parts.append("".join(current))
                current = []
            else:
                current.append(char)
        parts.append("".join(current))
        return [p.strip() for p in parts if p.strip()]

    def _get_triplet(self, color_str: str) -> ColorTriplet:
        color_str = color_str.strip().lower()
        if not color_str: return ColorTriplet(255, 255, 255)
        hex_val = self.COLORS.get(color_str, color_str)
        if hex_val.startswith("#"):
            try:
                h = hex_val.lstrip('#')
                if len(h) == 3: h = "".join(c*2 for c in h)
                return ColorTriplet(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            except: pass
        try:
            c = Color.parse(hex_val)
            if c.triplet: return c.triplet
            tc = c.get_truecolor()
            if tc.triplet: return tc.triplet
        except: pass
        return ColorTriplet(255, 255, 255)

    def _combine_styles(self, styles: List[Style]) -> Style:
        res = Style.null()
        for s in styles: res += s
        return res

    def parse(self, text: str) -> Text:
        result = Text()
        style_stack: List[Style] = []
        pos = 0
        while pos < len(text):
            match = self.tag_pattern.search(text, pos)
            if not match:
                result.append(text[pos:], style=self._combine_styles(style_stack))
                break
            if match.start() > pos:
                result.append(text[pos:match.start()], style=self._combine_styles(style_stack))
            
            tag_content = match.group(1)
            
            if tag_content.startswith("gradient:") or tag_content == "rainbow":
                remaining = text[match.end():]
                close_tag = "</gradient>" if tag_content.startswith("gradient:") else "</rainbow>"
                close_match = re.search(re.escape(close_tag) + r"|</>", remaining)
                
                if close_match:
                    inner_text = remaining[:close_match.start()]
                    colors = self.RAINBOW_COLORS if tag_content == "rainbow" else self._parse_tag_parts(tag_content)[1:]
                    # style_stack을 전달하여 외부 스타일(click 등)을 유지함
                    result.append(self._make_gradient(inner_text, colors, style_stack))
                    pos = match.end() + close_match.end()
                    continue

            self._handle_tag(tag_content, style_stack)
            pos = match.end()
        return result

    def _handle_tag(self, tag: str, stack: List[Style]):
        if tag == "/" or tag == "" or tag.startswith("/"):
            if stack: stack.pop()
            return
        parts = self._parse_tag_parts(tag)
        new_style = Style.null()
        skip_to = -1
        for i, part in enumerate(parts):
            if i <= skip_to: continue
            name = part.lower().strip()
            if name in self.COLORS or name.startswith("#"):
                new_style += Style(color=self.COLORS.get(name, name))
            elif name in ("bold", "b"): new_style += Style(bold=True)
            elif name in ("italic", "i", "em"): new_style += Style(italic=True)
            elif name in ("underlined", "u"): new_style += Style(underline=True)
            elif name in ("strikethrough", "st", "s"): new_style += Style(strike=True)
            elif name == "click":
                if len(parts) > i + 2:
                    action = parts[i+1].lower().strip()
                    value = parts[i+2].strip("'").strip()
                    if action == "open_url": new_style += Style(link=value)
                    skip_to = i + 2
        stack.append(new_style)

    def _make_gradient(self, text: str, color_strs: List[str], base_stack: List[Style]) -> Text:
        # 외부 스타일을 먼저 입힘
        base_style = self._combine_styles(base_stack)
        inner_parsed = self.parse(text)
        
        # 전체에 외부 스타일 적용
        inner_parsed.stylize(base_style)
        
        plain = inner_parsed.plain
        if not plain: return inner_parsed
        
        colors = [self._get_triplet(c) for c in color_strs if c.strip()]
        if len(colors) < 2:
            colors = colors * 2 if colors else [ColorTriplet(255,255,255), ColorTriplet(255,255,255)]
            
        res = Text()
        for i in range(len(plain)):
            char_text = inner_parsed[i] # 개별 글자의 스타일(외부+내부) 유지
            t = i / (len(plain) - 1) if len(plain) > 1 else 0
            num_segments = len(colors) - 1
            segment = min(int(t * num_segments), num_segments - 1)
            segment_t = (t * num_segments) - segment
            c1, c2 = colors[segment], colors[segment + 1]
            r = int(c1.red + (c2.red - c1.red) * segment_t)
            g = int(c1.green + (c2.green - c1.green) * segment_t)
            b = int(c1.blue + (c2.blue - c1.blue) * segment_t)
            
            # 그라데이션 색상을 추가 (기존 색상이 있다면 덮어씌움)
            char_text.stylize(Style(color=f"#{r:02x}{g:02x}{b:02x}"))
            res.append_text(char_text)
        return res

def parse(text: str) -> Text:
    return MiniMessageParser().parse(text)
