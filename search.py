import pandas as pd
import argparse
import ast


def search_dataset(first, second):
    while not (moves_data['Move'] == first.upper()).any():
        print(first, 'not found')
        print('First Move?')
        first = str(input())

    while not (moves_data['Move'] == second.upper()).any():
        print(second, 'not found')
        print('Second Move?')
        second = str(input())

    f_pokes = moves_data[moves_data['Move'] == first.upper()]['Pokemon'].values[0]
    s_pokes = moves_data[moves_data['Move'] == second.upper()]['Pokemon'].values[0]

    vc = pd.Series(f_pokes + s_pokes).value_counts()
    res = vc[vc > 1].index.tolist()

    if len(res) < 1:
        print('No pokemon have access to both moves.')
        print(first, "is learnt by:", f_pokes)
        print(second, "is learnt by:", s_pokes)
    else:
        print('These pokemon can learn both moves:', vc[vc > 1].index.tolist())





moves_data = pd.read_csv('latest.csv', header=0)

moves_data['Pokemon'] = moves_data['Pokemon'].apply(lambda x: ast.literal_eval(x))
moves_data['Move'] = moves_data['Move'].apply(lambda x: str(x).upper())

parser = argparse.ArgumentParser()
parser.add_argument('first')
parser.add_argument('second')

parsed_args = parser.parse_args()
x = parsed_args.first
y = parsed_args.second


while True:
    search_dataset(x, y)
    input('Press a key to search again')
    replace = int(input('Which move to replace? 0 (both), 1 (first), 2 (second)'))
    if replace is 0 or replace is 1:
        x = str(input('New First Move?'))
    if replace is 0 or replace is 2:
        y = str(input('New Second move?'))