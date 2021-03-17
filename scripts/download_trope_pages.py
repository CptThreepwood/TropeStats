from config import TROPE_INDEX

import parsing.parse_html as parse

KNOWN_TROPES = parse.load_config(TROPE_INDEX)

if __name__ == '__main__':
    for trope in KNOWN_TROPES:
        print(trope)
        download_and_store(trope)
