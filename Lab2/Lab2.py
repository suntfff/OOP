from enum import Enum
import json, os, sys


class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    WHITE = "\033[97m"
    BLACK = "\033[30m"
    YELLOW = "\033[33m"
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;205m"
    PURPLE = "\033[35m"
    RESET = "\033[0m"

class FontLoader:
    _fonts = None

    @classmethod
    def get_fonts(cls) -> dict:
        if cls._fonts is None:
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, 'Fonts.json')
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл '{file_path}' не найден.")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cls._fonts = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Ошибка при разборе JSON из файла '{file_path}': {e}")
            except Exception as e:
                raise RuntimeError(f"Не удалось загрузить шрифты: {e}")
        
        return cls._fonts
class Printer:
    def __init__(self, color: Color = Color.WHITE, position: tuple[int, int]  = (1,1), symbol: str = '*') -> None:
        self._color = color
        self._symbol = symbol
        self._fonts = None
        self._base_position_x = position[0]
        self._base_position_y = position[1]
        self._position_x = self._base_position_x
        self._position_y = self._base_position_y

    @classmethod
    def print_static(cls, text: str, color  = Color.WHITE, position: tuple[int, int]  = (1,1), symbol: str = '*') -> None:
        pos_x, pos_y = position
        text = text.upper()
        fonts = FontLoader.get_fonts()
        height = len(next(iter(fonts.values())))
        sys.stdout.write(f"\033[{pos_y};{pos_x}H")
        sys.stdout.write(color.value)
        for row in range(height):
            for ch in text:
                line = fonts[ch][row]
                for bit in line:
                    sys.stdout.write(symbol if bit == '1' else ' ')
            pos_y += 1
            sys.stdout.write(f"\033[{pos_y};{pos_x}H")
        sys.stdout.write(Color.RESET.value)

    def print_dynamic(self, text: str) -> None:
        if self._fonts is None:
            raise RuntimeError("Шрифты не загружены. Используй Printer в блоке 'with'.")
        sys.stdout.write(f"\033[{self._position_y};{self._position_x}H")
        sys.stdout.write(self._color.value)
        text = text.upper()
        height = len(next(iter(self._fonts.values())))
        for row in range(height):
            for char in text:
                line = self._fonts[char][row]
                for symbol in line:
                    sys.stdout.write(self._symbol if symbol == '1' else ' ')
            self._position_y+=1
            sys.stdout.write(f"\033[{self._position_y};{self._position_x}H")
        self._position_y+=1

    def __enter__(self)  -> "Printer":
        self._fonts = FontLoader.get_fonts()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        sys.stdout.write(Color.RESET.value)
        sys.stdout.write("\033[1;1H")
        return False




if __name__ == "__main__":
    with Printer(Color.GREEN , (13, 5), '*') as printer:
        printer.print_dynamic('ичт')
        printer.print_dynamic('аба')

    Printer.print_static('ехе', Color.GREEN , (25, 5), '?')

    sys.stdout.write("\033[1;1H")
    os.system('cls')
    
