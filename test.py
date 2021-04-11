"""
Some tests to run
"""
from random import randint
from jerocat import Jerocat

if __name__ == '__main__':
    print("inici")
    j = Jerocat()

    # creem usuari
    u1 = j.user_add(id=0, username="jerocatbot")


    # creem jocs
    for ng in range(10):
        g = j.game_add(name="g"+str(ng), user=u1, status=j.STATUS_PUBLIC)
        for nq in range(randint(10, 40)):
            q = j.question_add(game=g, question=g.name+"_q"+str(nq))
            for na in range(randint(1, 3)):
                a = j.answer_add(question=q, answer=q.text+"_a"+str(na))

    gs = j.game_list()


    for n in range(40,randint(40,100)):
        g = j.game_get(randint(1, len(gs)))
        for n in range(randint(10, 20)):
            #intentem una respostes
            for a in range(4*len(g.questions)):
                j.answer_check(g, 1, a)


#     for q in g.questions:
#         print(str(q.id)+" "+q.text +
#               " [" + ', '.join([str(a.text) for a in q.answers])+"]")
    