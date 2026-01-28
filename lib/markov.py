import collections, random, textwrap, re
from pathlib import Path

class MarkovGenerator:

    @staticmethod
    def _normalize(word: str):
        word = word.replace("\"","")
        word = word.replace("”","")
        word = word.replace("“","")
        word = word.replace("_","")
        return word

    @staticmethod
    def run():

        base = Path(__file__).resolve().parent.parent
        file_path = base / 'static' / 'commedia.txt'
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Build possibles table indexed by pair of prefix words (w1, w2)
        w1 = w2 = w3 = ''
        possibles = collections.defaultdict(list)
        with file_path.open('r', encoding='utf-8') as file:
            for line in file:
                for word in line.split():
                    word = MarkovGenerator._normalize(word)
                    possibles[w1, w2, w3].append(word)
                    w1, w2, w3 = w2, w3, word

        # Avoid empty possibles lists at end of input
        possibles[w1, w2, w3].append('')
        possibles[w2, w3, ''].append('')
        possibles[w3, '', ''].append('')

        # Generate randomized output (start with a random capitalized prefix)
        w1, w2, w3 = random.choice([k for k in possibles if k[0][:2].isupper()])
        output = [w1, w2, w3]

        for _ in range(int(50)):
            word = random.choice(possibles[w1, w2, w3])
            output.append(word)
            w1, w2, w3 = w2, w3, word

        # Print output wrapped to 70 columns
        result = textwrap.fill(' '.join(output))
        regex_pattern = r"[;.!]"
        return re.split(regex_pattern, result)[0]