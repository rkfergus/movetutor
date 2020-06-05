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
        return False, [f_pokes, s_pokes]
    else:
        return True, [res]


def search_all(list_of_moves):
    vc = list()
    for move in list_of_moves:
        filtered = moves_data[moves_data['Move'] == move.upper()]['Pokemon'].values[0]
        vc = vc + filtered
    vc = pd.Series(vc).value_counts()
    return vc[vc >= len(list_of_moves)].index.tolist()


def search_all_of_and_any(all_list, any_list):
    all_result = search_all(all_list)
    matches = pd.DataFrame(columns=['Pokemon', 'Move'])
    for move in any_list:
        try:
            pokes = moves_data[moves_data['Move'] == move.upper()]['Pokemon'].values[0]
            vc = pd.Series(pokes + all_result).value_counts()
            df = pd.DataFrame({'Pokemon': vc[vc > 1].index, 'Move': move})
            if len(df) > 0:
                matches = matches.append(df, ignore_index=True).sort_values('Pokemon')
        except IndexError:
            print('No move found matching', move)
    return matches


def search_multi_any(all_list, any_lists):
    sub_matches = list()
    for li in any_lists:
        sub_matches.append(search_all_of_and_any(all_list, li))

    pokes = list()
    for df in sub_matches:
        pokes = pokes + df['Pokemon'].unique().tolist()

    if len(pokes) > 0:
        pokes = pd.Series(pokes).value_counts()
        print(pokes)
        pokes = pokes[pokes >= len(any_lists)].index.tolist()
        guide = pd.DataFrame()
        guide['Pokemon'] = pokes
        for i in range(0, len(sub_matches)):
            col_name = 'Move Set ' + str(i + 1)
            df = sub_matches[i]
            guide.insert(i+1, col_name, guide['Pokemon'].apply(lambda x: df[df['Pokemon'] == x]['Move'].tolist()))
        return guide
    else:
        print('No pokemon found matching the requirements.')
        return sub_matches


def search_of_any(first, list_of_moves):
    guide = pd.DataFrame(columns=['Pokemon', 'Move'])
    for move in list_of_moves:
        res, lists = search_dataset(first, move)
        if res:
            df = pd.DataFrame({'Pokemon': lists[0], 'Move': move})
            guide = guide.append(df, ignore_index=True).sort_values('Pokemon')
    return guide


moves_data = pd.read_csv('latest.csv', header=0)

moves_data['Pokemon'] = moves_data['Pokemon'].apply(lambda x: ast.literal_eval(x))
moves_data['Move'] = moves_data['Move'].apply(lambda x: str(x).upper())
pd.set_option('display.max_columns', 500)
# parser = argparse.ArgumentParser()
# parser.add_argument('first')
# parser.add_argument('second')
#
# parsed_args = parser.parse_args()
# f = parsed_args.first
# s = parsed_args.second
#
#
# while True:
#     search_dataset(f, s)
#     input('Press a key to search again')
#     replace = int(input('Which move to replace? 0 (both), 1 (first), 2 (second)'))
#     if replace is 0 or replace is 1:
#         f = str(input('New First Move?'))
#     if replace is 0 or replace is 2:
#         s = str(input('New Second move?'))
