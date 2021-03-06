from jerocat import Jerocat

if __name__ == '__main__':
    print("inici")
    j = Jerocat()

    # creem usuari
    u1 = j.user_add(uid=0, name="jerocatbot")

    # creem dos jocs
    g1 = j.game_add(name="Plats de cuina catalana",user=u1)

    # Els hi posem preguntes
    q = j.question_add(game=g1, question="🛡️👉👩‍🦰");
    a = j.answer_add(question=q, answer="Escudella")
    q = j.question_add(game=g1, question="🦶🦶🐷 + 🦵🚱");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🏠👉🤴👸🏻d🐟");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="👅🐃");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🦢🍐🍐🍷");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔪🥮👈⭕️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥯👑👑👑");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="1000 🌿☘️🍃d🍄🍄");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🐵d🗿");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥗d 💴💶💴");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🅰️👦🍯🧸+🎺🎺⚰️✝️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="(🍧🥧🍮)d🎶🎷🎸");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 👙");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🔊🥖d🔚🎲🎲a--->e");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥔🥔 o 🔦");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" (🇬🇧🐭-a) d 🍫🍊");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🅰️👦⛩️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🚃-go🤫+🦵🟡🟡");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🔊🥖🥶 d 🍉");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥙🧀🐐");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥧🧀+🍯🧚‍♀️🍓");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🔥ll*ll");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🅰️👦+🥛🍼");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 👠👡👢👟a--->o");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥙d🍅i 🧅🥊💥👊");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 💪d👨🏽‍🎤");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="💩a-->o d 👼 joan");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="(🥖🤷‍♂️🥖) d🧀");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥚🥚🥚👉🍽️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥖d 😫👌d🍷c");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🐙 🧚‍♀️(🇫🇷) (🛣️🏃‍♂️🇪🇸)");
    #a = j.answer_add(question=q, answer="")



    gs = j.game_list()
    for g in gs:
        print(str(g.name))
        for q in g.questions:
            print("q:"+str(q.name))
            for a in q.answers:
                print("a:"+str(a.name))
