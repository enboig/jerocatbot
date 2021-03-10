"""
Some tests to run
"""

from jerocat import Jerocat

if __name__ == '__main__':
    print("inici")
    j = Jerocat()

    gs = j.game_list()

    for key, value in gs.items():
        print(str(key)+": "+value)

    g=j.game_get(1)
    print(g.name)
    for q in g.questions:
        print(str(q.id)+q.name)