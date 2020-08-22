import argparse


parser = argparse.ArgumentParser(
    description='Описание как работать с программой'
)
parser.add_argument('-l','--link', help='Ссылка / Битлинк')
args = parser.parse_args()
print(args.link)
