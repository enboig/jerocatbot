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

    g = j.game_get(1)
    print(g.name)
    for q in g.questions:
        print(str(q.id)+" "+q.text +
              " [" + ', '.join([str(a.text) for a in q.answers])+"]")

    print(g.name)

    q = 1
    a = "manresa"
    print(j.question_get(g, q).text+": " + a + " --> " +
          ("correcte" if j.answer_check(g, 1, a) else "erroni"))

    q = 1
    a = "ManResa"
    print(j.question_get(g, q).text+": " + a + " --> " +
          ("correcte" if j.answer_check(g, 1, a) else "erroni"))

    q = 1
    a = "Manrusia"
    print(j.question_get(g, q).text+": " + a + " --> " +
          ("correcte" if j.answer_check(g, 1, a) else "erroni"))
