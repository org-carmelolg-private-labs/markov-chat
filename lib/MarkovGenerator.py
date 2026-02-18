import random, textwrap
from pathlib import Path

from collections import defaultdict, deque
from lib.EnvironmentVariables import EnvironmentVariables
from lib.StringUtils import normalize, substring

env = EnvironmentVariables()

class MarkovGenerator:

    @staticmethod
    def run():
        if env.get_temperature(1) >= 0.5:
            return MarkovGenerator._creative()
        else:
            return MarkovGenerator._deterministic()


    @staticmethod
    def _file_path():
        base = Path(__file__).resolve().parent.parent
        paths = []
        for filename in env.get_input_filename():
            paths.append(base / 'static' / filename)
        return paths

    @staticmethod
    def _read_words(file_paths):
        for file_path in file_paths:
            with file_path.open('r', encoding='utf-8') as file:
                for line in file:
                    for word in line.split():
                        normalized = normalize(word)
                        if normalized is not None:
                            yield normalized

    @staticmethod
    def _build_possibles(prefix_len: int):
        file_paths = MarkovGenerator._file_path()
        if len(file_paths) == 0:
            raise FileNotFoundError(f"File empty")

        for file_path in file_paths:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

        possibles = defaultdict(list)
        dq = deque([''] * prefix_len, maxlen=prefix_len)
        for word in MarkovGenerator._read_words(file_paths):
            possibles[tuple(dq)].append(word)
            dq.append(word)

        # Fill tail keys with empty terminator to avoid missing keys
        tail = list(dq)
        for _ in range(prefix_len):
            possibles[tuple(tail)].append('')
            tail = tail[1:] + ['']

        return possibles

    @staticmethod
    def _pick_start_key(possibles):
        # Prefer keys whose first element starts with an uppercase letter
        candidates = [k for k in possibles.keys() if k[0] and k[0][0].isupper()]
        if not candidates:
            candidates = [k for k in possibles.keys() if k[0]]
        if not candidates:
            candidates = list(possibles.keys())
        return random.choice(candidates)

    @staticmethod
    def _generate(possibles, start_key, max_words):
        key = tuple(start_key)
        output = list(key)

        for _ in range(int(max_words)):
            choices = possibles.get(key, [''])
            word = random.choice(choices)
            output.append(word)
            key = tuple(list(key[1:]) + [word]) if len(key) > 1 else (word,)

        return substring(textwrap.fill(' '.join(output)), ';.!')

    @staticmethod
    def _deterministic():
        possibles = MarkovGenerator._build_possibles(prefix_len=3)
        start_key = MarkovGenerator._pick_start_key(possibles)
        return MarkovGenerator._generate(possibles, start_key, env.get_max_words(50))

    @staticmethod
    def _creative():
        possibles = MarkovGenerator._build_possibles(prefix_len=2)
        start_key = MarkovGenerator._pick_start_key(possibles)
        return MarkovGenerator._generate(possibles, start_key, env.get_max_words(50))
