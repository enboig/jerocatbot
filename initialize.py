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
    q = j.question_add(game=g1, question="🦶🦶🐷+🦵🚱");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🏠👉🤴👸🏻d🐟");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="👅🐃");
    a = j.answer_add(question=q, answer="Llengua de bou")
    q = j.question_add(game=g1, question="🦢🍐🍐🍷");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔪🥮👈⭕️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥯👑👑👑");
    a = j.answer_add(question=q, answer="Tortell de Reis")
    q = j.question_add(game=g1, question="1000 🌿☘️🍃d🍄🍄");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🐵d🗿");
    a = j.answer_add(question=q, answer="Mona de Pasqua")
    q = j.question_add(game=g1, question=" 🥗d 💴💶💴");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🅰️👦🍯🧸+🎺🎺⚰️✝️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="(🍧🥧🍮)d🎶🎷🎸");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="👙");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔊🥖d🔚🎲🎲a--->e");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥔🥔 o 🔦");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="(🇬🇧🐭-a) d 🍫🍊");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🅰️👦⛩️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🚃-go🤫+🦵🟡🟡");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔊🥖🥶 d 🍉");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🥙🧀🐐");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥧🧀+🍯🧚‍♀️🍓");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔥ll*ll");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🅰️👦+🥛🍼");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="👠👡👢👟a--->o");
    a = j.answer_add(question=q, answer="Calçots")
    q = j.question_add(game=g1, question="🥙d🍅i 🧅🥊💥👊");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="💪d👨🏽‍🎤");
    a = j.answer_add(question=q, answer="Braç de gitano")
    q = j.question_add(game=g1, question="💩a-->o d 👼 joan");
    a = j.answer_add(question=q, answer="Coca de Sant Joan")
    q = j.question_add(game=g1, question="(🥖🤷‍♂️🥖) d🧀");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥚🥚🥚👉🍽️");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🥖d 😫👌d🍷c");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question=" 🐙 🧚‍♀️(🇫🇷) (🛣️🏃‍♂️🇪🇸)");
    #a = j.answer_add(question=q, answer="")


    g = j.game_add(name="Varietats de raïm",user=u1)
    #q = j.question_add(game=g1, question="");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="Gr🦵🏻⚪️")
    a = j.answer_add(question=q, answer="Garnatxa blanca")
    q = j.question_add(game=g1, question="Gr 🦵🏻 ⚫️")
    a = j.answer_add(question=q, answer="Granatxa negra")
    q = j.question_add(game=g1, question="👁🐇")
    a = j.answer_add(question=q, answer="Ull de llebre")
    q = j.question_add(game=g1, question="𓆦🍵")
    a = j.answer_add(question=q, answer="Moscatell")
    q = j.question_add(game=g1, question="★👨🏻‍✈️9")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="✋🏻K🗣")
    a = j.answer_add(question=q, answer="Macabeu")
    q = j.question_add(game=g1, question="🐑R🌯")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="3⃣🥖T")
    a = j.answer_add(question=q, answer="Trepat")
    q = j.question_add(game=g1, question="🟢👇🏻")
    a = j.answer_add(question=q, answer="Verdot petit")
    q = j.question_add(game=g1, question="🏞🍷🧝🏼‍♂ ⚪️")
    a = j.answer_add(question=q, answer="Sauvignon Blanc")
    q = j.question_add(game=g1, question="💩🔦")
    a = j.answer_add(question=q, answer="Merlot")
    q = j.question_add(game=g1, question="🎼🎼🎼🎼🎼🎼🎼☀️🛐")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="👫DA")
    a = j.answer_add(question=q, answer="Parellada")
    q = j.question_add(game=g1, question="👨🏻‍🍳🍷")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="✋🏻N🎶  ⚫️")
    a = j.answer_add(question=q, answer="Manto negre")
    q = j.question_add(game=g1, question="🗞  ⚪️   De  ✋🏻LL🐋")
    a = j.answer_add(question=q, answer="Premsal Blanc de Mallorca")
    q = j.question_add(game=g1, question="🌶( 🏞🍷🧝🏼‍♂)")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🌊🌌🐜 o (2x17)")
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🔨🐥")
    a = j.answer_add(question=q, answer="Picapoll")

    g = j.game_add(name="Caves de Sant Sadurní",user=u1)
    #q = j.question_add(game=g1, question="");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="🎄⭐️");
    q = j.question_add(game=g1, question="👨🏻‍🦳🌳🍈");
    q = j.question_add(game=g1, question="🅰️🍵🚽");
    q = j.question_add(game=g1, question="🍚🐒");
    q = j.question_add(game=g1, question="⛲️🌲🛁");
    q = j.question_add(game=g1, question="🎵💸E🎵");
    q = j.question_add(game=g1, question="🗼🗼");
    q = j.question_add(game=g1, question="👩🏼‍🏫👨🏻‍🏫");
    q = j.question_add(game=g1, question="🗼🐺➖🅿️");
    q = j.question_add(game=g1, question="🟢🍾➖🅿️ (👧)");
    q = j.question_add(game=g1, question="👨🏻‍🦳🦁");
    q = j.question_add(game=g1, question="👨🏻‍🦳🗼🐺➖🅿️🔫");
    q = j.question_add(game=g1, question="🐺🎨");
    q = j.question_add(game=g1, question="🏘🎨🚀");
    q = j.question_add(game=g1, question="🍐💨👉🏻Ra");
    q = j.question_add(game=g1, question="🖥I🐄NE");
    q = j.question_add(game=g1, question="⚪️🪑");
    q = j.question_add(game=g1, question="CO🚪❌1️⃣");
    q = j.question_add(game=g1, question="🆓XE🛁");
    q = j.question_add(game=g1, question="👨🏼‍🦳♻️♻️");
    q = j.question_add(game=g1, question="🛕⚪️");
    q = j.question_add(game=g1, question="🏰    DE  🗻🐶");
    q = j.question_add(game=g1, question="⛰🎿US");
    q = j.question_add(game=g1, question="👦🏻 I 🏞");
    q = j.question_add(game=g1, question="🖥 I ⛪️");
    q = j.question_add(game=g1, question="📜🎤🎨");
    q = j.question_add(game=g1, question="AL👀🧄");
    q = j.question_add(game=g1, question="🛕🔥👩🏼");
    q = j.question_add(game=g1, question="L’💰❗️🔫");
    q = j.question_add(game=g1, question="🌊IA RI🥅⚽️💻");
    q = j.question_add(game=g1, question="👦🏻✋🏻🍏🍑🍒👩🏼");
    q = j.question_add(game=g1, question="🕊👉🏼🧒");
    q = j.question_add(game=g1, question="🏪🍺 i 🃏");
    q = j.question_add(game=g1, question="🌞E 👦🏻");
    q = j.question_add(game=g1, question="ES🍯");
    q = j.question_add(game=g1, question="💨👉🏻RA🌞ER");
    q = j.question_add(game=g1, question="RA💨🗣I⚪️");
    q = j.question_add(game=g1, question="🏡🌲🍈");
    q = j.question_add(game=g1, question="🏰👩🏻‍🦰");
    q = j.question_add(game=g1, question="👦🏼👈🏻I ♦️🐻A");
    q = j.question_add(game=g1, question="🌊IA🏠🚫VAS");
    q = j.question_add(game=g1, question="🏰⚪️");
    q = j.question_add(game=g1, question="MUS🏡🌞");
    q = j.question_add(game=g1, question="🌎🃏TELL");
    q = j.question_add(game=g1, question="🏡💶🃏");
    q = j.question_add(game=g1, question="👨🏼‍🦳");
    q = j.question_add(game=g1, question="👮🏻‍♂️👵🏻⚫️");
    q = j.question_add(game=g1, question="🏡TI💍");
    q = j.question_add(game=g1, question="NA🟩🐜");
    q = j.question_add(game=g1, question="💂🏼‍♀️🌎IS🧟‍♀️");
    q = j.question_add(game=g1, question="CO🍷DES");
    q = j.question_add(game=g1, question="🌲 I 💃🏼🕺🏻");
    q = j.question_add(game=g1, question="🏡ET");
    q = j.question_add(game=g1, question="🍐L🧚🏻");
    q = j.question_add(game=g1, question="➕🗻");
    q = j.question_add(game=g1, question="👩🏼🟢🛁");
    q = j.question_add(game=g1, question="🏰 DE 👼👱🏻‍♂️");
    q = j.question_add(game=g1, question="⛲️ JUI");

    g = j.game_add(name="Pel·lícules",user=u1)
    #q = j.question_add(game=g1, question="");
    #a = j.answer_add(question=q, answer="")
    q = j.question_add(game=g1, question="😊😊😢😢");
    a = j.answer_add(question=q, answer="Sonrisas y lágrimas");
    q = j.question_add(game=g1, question="🎤☔️");
    q = j.question_add(game=g1, question="📖🌴");
    q = j.question_add(game=g1, question="👻🎼");
    q = j.question_add(game=g1, question="🤫🐑🐑🐑🐑");
    q = j.question_add(game=g1, question="🌏🐒🐒🐒");
    q = j.question_add(game=g1, question="👼👼👿😈");
    q = j.question_add(game=g1, question="☕️🥐💎💎");
    q = j.question_add(game=g1, question="💍💍💍💍⚰️");
    q = j.question_add(game=g1, question="🔓🌅");


    g = j.game_add(name="Places, carrers i llocs de Sant Sadurní",user=u1)
    #q = j.question_add(game=g1, question="");
    q = j.question_add(game=g1, question="⛰️🔪");
    q = j.question_add(game=g1, question="⛪️");
    q = j.question_add(game=g1, question="🎥⛳️🕋🙋🏼‍♂️");
    q = j.question_add(game=g1, question="🗣️❗️🤚🏻🧍‍♀️");
    q = j.question_add(game=g1, question="🎵👀🚫");
    q = j.question_add(game=g1, question="🏘️®️🛸");
    q = j.question_add(game=g1, question="🌼🌼");
    q = j.question_add(game=g1, question="🏘️🚫🏦");
    q = j.question_add(game=g1, question="🏠🏠🥼🏥");
    q = j.question_add(game=g1, question="⛲️👉🏍️");
    q = j.question_add(game=g1, question="💪®️🐣");
    q = j.question_add(game=g1, question="⏫©️🅰️");
    q = j.question_add(game=g1, question="👳‍♀️🐶");
    q = j.question_add(game=g1, question="📄📄📄");
    q = j.question_add(game=g1, question="🎡🎢💐🗣️");
    q = j.question_add(game=g1, question="🕌🅾️");
    q = j.question_add(game=g1, question="⏬©️🅰️");
    q = j.question_add(game=g1, question="➕3️⃣🕋🙋🏼‍♂️");
    q = j.question_add(game=g1, question="🐱🚬");
    q = j.question_add(game=g1, question="👀");
    q = j.question_add(game=g1, question="🐶✝️®️👉🏡");
    q = j.question_add(game=g1, question="🌉🚉");
    q = j.question_add(game=g1, question="🎡🎢🎵👀🚫");
    q = j.question_add(game=g1, question="🏬🏬🗣️👂");
    q = j.question_add(game=g1, question="🌉®️🤚🏻");
    q = j.question_add(game=g1, question="😇🍐");
    q = j.question_add(game=g1, question="🏥");
    q = j.question_add(game=g1, question="🖕🅿️🚉");
    q = j.question_add(game=g1, question="🏭");
    q = j.question_add(game=g1, question="🤝🏯🏯");
    q = j.question_add(game=g1, question="🧊🌬️");
    q = j.question_add(game=g1, question="⛲️✝️");
    q = j.question_add(game=g1, question="🏟️🦊");
    q = j.question_add(game=g1, question="🎵🏭🧱");
    q = j.question_add(game=g1, question="🌍🖕");
    q = j.question_add(game=g1, question="↪️🌊");
    q = j.question_add(game=g1, question="🕋🌊");
    q = j.question_add(game=g1, question="🏚️🍻☄️🌊");
    q = j.question_add(game=g1, question="😇5️⃣❗️");
    q = j.question_add(game=g1, question="🏄‍♀️🥇👉🧍‍♂️");
    q = j.question_add(game=g1, question="ℹ️🇬🇧🕋");
    q = j.question_add(game=g1, question="🏟️🇪🇺");
    q = j.question_add(game=g1, question="👨‍🔬🏚️®️");
    q = j.question_add(game=g1, question="🏬⛪️🏫🏥👉🧍‍♀️");
    q = j.question_add(game=g1, question="🌹🌹🌹");

    g = j.game_add(name="Poblacions del Penedès",user=u1)
    #q = j.question_add(game=g1, question="");
    q = j.question_add(game=g1, question="🥇⬆️");
    a = j.answer_add(question=q, answer="Ordal");
    q = j.question_add(game=g1, question="🕌🍷🎵📍");
    a = j.answer_add(question=q, answer="Castellví de la marca");
    q = j.question_add(game=g1, question="🧊🌬");
    a = j.answer_add(question=q, answer="Gelida");
    q = j.question_add(game=g1, question="😇🤝🥇⬆️");
    a = j.answer_add(question=q, answer="Sant Pau d'Ordal");
    q = j.question_add(game=g1, question="😇🌼👲👲");
    a = j.answer_add(question=q, answer="Sta Margarida i els Monjos");
    q = j.question_add(game=g1, question="😇🌈🚽");
    a = j.answer_add(question=q, answer="Sant Martí Sarroca");
    q = j.question_add(game=g1, question="🌉🐀🐀");
    a = j.answer_add(question=q, answer="Pontons");
    q = j.question_add(game=g1, question="🐰🐰");
    a = j.answer_add(question=q, answer="Conilleres");
    q = j.question_add(game=g1, question="🐶🤘");
    a = j.answer_add(question=q, answer="Les Cabanyes");
    q = j.question_add(game=g1, question="⛲️💍");
    a = j.answer_add(question=q, answer="Font-Rubí");
    q = j.question_add(game=g1, question="🐷🏄‍♀");
    a = j.answer_add(question=q, answer="Sardinyola");
    q = j.question_add(game=g1, question="🏘🦊🦊");
    a = j.answer_add(question=q, answer="Viladellops");
    q = j.question_add(game=g1, question="💃®️🌊");
    a = j.answer_add(question=q, answer="Olèrdola");
    q = j.question_add(game=g1, question="⛰👉🧍");
    a = j.answer_add(question=q, answer="Montmell");
    q = j.question_add(game=g1, question="😇🍸");
    a = j.answer_add(question=q, answer="Santa Oliva");
    q = j.question_add(game=g1, question="©️🕴🐛");
    a = j.answer_add(question=q, answer="Comarruga");
    q = j.question_add(game=g1, question="😇🌞🍆🥒🧅");
    a = j.answer_add(question=q, answer="Sant Llorenç d'Hortons");
    q = j.question_add(game=g1, question="🕋🎵🍇");
    a = j.answer_add(question=q, answer="Torrelavit");
    q = j.question_add(game=g1, question="🌍🌊");
    a = j.answer_add(question=q, answer="Mediona");
    q = j.question_add(game=g1, question="📈❗️🧶");
    a = j.answer_add(question=q, answer="Subirats");
    q = j.question_add(game=g1, question="😇🍐👜®️");
    a = j.answer_add(question=q, answer="Sant Pere Sacarrera");
    q = j.question_add(game=g1, question="😇🍐🌉🎳");
    a = j.answer_add(question=q, answer="Sant Pere de Riudebitlles");
    q = j.question_add(game=g1, question="🏘🚫🏦🅿️");
    a = j.answer_add(question=q, answer="Vilafranca del Penedès");
    q = j.question_add(game=g1, question="😇🪐👉👱‍♀");
    a = j.answer_add(question=q, answer="Sant Sadurní d'Anoia");
    q = j.question_add(game=g1, question="😇5⃣❗️🌍🌊");
    a = j.answer_add(question=q, answer="Sant Quintí de Mediona");
    q = j.question_add(game=g1, question="😇🏄‍♀🧂");
    a = j.answer_add(question=q, answer="Sant Marçal");
    q = j.question_add(game=g1, question="🎵🏃‍♀");
    a = j.answer_add(question=q, answer="La Ràpita");
    q = j.question_add(game=g1, question="🏠⚪️");
    a = j.answer_add(question=q, answer="Casablanca");
    q = j.question_add(game=g1, question="👉➖🅿️");
    a = j.answer_add(question=q, answer="El Pla del Penedès");
    q = j.question_add(game=g1, question="😇✝️🅿️");
    a = j.answer_add(question=q, answer="Santa Fe del Penedès");
    q = j.question_add(game=g1, question="😇🧅🧅🧍‍♀🟡");
    a = j.answer_add(question=q, answer="Sant Sebastià dels Gorgs");
    q = j.question_add(game=g1, question="🕋💐🌊");
    a = j.answer_add(question=q, answer="Torreramona");
    q = j.question_add(game=g1, question="🎵⛰🔘");
    a = j.answer_add(question=q, answer="La Muntanya Rodona");
    q = j.question_add(game=g1, question="♂✔️🔚®️👤");
    a = j.answer_add(question=q, answer="El Vendrell");
    q = j.question_add(game=g1, question="🏠🔴");
    a = j.answer_add(question=q, answer="Can Roig");
    q = j.question_add(game=g1, question="☀️🅿️");
    a = j.answer_add(question=q, answer="Llorenç del Penedès");
    q = j.question_add(game=g1, question="🎵🐝");
    a = j.answer_add(question=q, answer="L'Avellà");
    q = j.question_add(game=g1, question="🍷🅾️🍷🅿️");
    a = j.answer_add(question=q, answer="Vilobí del Penedès");
    q = j.question_add(game=g1, question="🎵⛲️🌲🌲🌲");
    a = j.answer_add(question=q, answer="La Font del Bosc");
    q = j.question_add(game=g1, question="⬆️🏄‍♂");
    a = j.answer_add(question=q, answer="Daltmar");
    q = j.question_add(game=g1, question="🎵💣🅿️");
    a = j.answer_add(question=q, answer="La Granada del Penedès");
    q = j.question_add(game=g1, question="🛁🛁🅿️");
    a = j.answer_add(question=q, answer="Banyeres del Penedès");
    q = j.question_add(game=g1, question="🐶📦");
    a = j.answer_add(question=q, answer="Can Cartró");
    q = j.question_add(game=g1, question="🗣🎤🦊🦊");
    a = j.answer_add(question=q, answer="Cantallops");
    q = j.question_add(game=g1, question="🐶🐑🚿🎵🛳");
    a = j.answer_add(question=q, answer="Can Benet de la Prua");
    q = j.question_add(game=g1, question="⛰🌲");
    a = j.answer_add(question=q, answer="Puigdàlber");
    q = j.question_add(game=g1, question="🔨👭🏞");
    #a = j.answer_add(question=q, answer="");
    q = j.question_add(game=g1, question="🏠🙎‍♂👤⛰⛰⛰");
    #a = j.answer_add(question=q, answer="";

    g = j.game_add(name="Bars i restaurants de Sant Sadurní d'Anoia",user=u1)
    #q = j.question_add(game=g1, question="");
    q = j.question_add(game=g1, question="🌳");
    a = j.answer_add(question=q, answer="el pino");
    q = j.question_add(game=g1, question="🥶🥵");
    a = j.answer_add(question=q, answer="fred i calent");
    q = j.question_add(game=g1, question="🍷👍🏽");
    a = j.answer_add(question=q, answer="vibop");
    q = j.question_add(game=g1, question="🇽🇹");
    a = j.answer_add(question=q, answer="dallas");
    q = j.question_add(game=g1, question="🥁");
    a = j.answer_add(question=q, answer="tabalots");
    q = j.question_add(game=g1, question="🦪");
    a = j.answer_add(question=q, answer="la perla");
    q = j.question_add(game=g1, question="🍽🍽");
    q = j.question_add(game=g1, question="🤵🏽👌");
    a = j.answer_add(question=q, answer="selecte");
    q = j.question_add(game=g1, question="🍾🍾🌳");
    a = j.answer_add(question=q, answer="taps de suro");
    q = j.question_add(game=g1, question="☕️");
    a = j.answer_add(question=q, answer="el cafè");
    q = j.question_add(game=g1, question="🍱");
    a = j.answer_add(question=q, answer="homu");
    q = j.question_add(game=g1, question="2⃣2⃣");
    a = j.answer_add(question=q, answer="el 22");
    q = j.question_add(game=g1, question="🎯");
    a = j.answer_add(question=q, answer="el centre");
    q = j.question_add(game=g1, question="🦽");
    a = j.answer_add(question=q, answer="la roda");
    q = j.question_add(game=g1, question="💃🏽💃🏽");
    a = j.answer_add(question=q, answer="al alandalus");
    q = j.question_add(game=g1, question="🌞🍷");
    a = j.answer_add(question=q, answer="sol i vi");
    q = j.question_add(game=g1, question="🌯");
    a = j.answer_add(question=q, answer="donner");
    q = j.question_add(game=g1, question="🏡👴🏼🌊");
    q = j.question_add(game=g1, question="🗣👍");
    q = j.question_add(game=g1, question="👩‍🦯 🥶");
    a = j.answer_add(question=q, answer="segafredo");
    q = j.question_add(game=g1, question="🏑");
    a = j.answer_add(question=q, answer="l'Ateneu");
    q = j.question_add(game=g1, question="🤷🏽‍♂🙆🏽‍♀🙅🏼‍♀💁🏽‍♂🧵");
    q = j.question_add(game=g1, question="🔔");
    a = j.answer_add(question=q, answer="picarol");
    q = j.question_add(game=g1, question="🔔🇮🇹");
    a = j.answer_add(question=q, answer="il picarolo");
    q = j.question_add(game=g1, question="🌊🤣");
    q = j.question_add(game=g1, question="⛔️");
    a = j.answer_add(question=q, answer="sentit contrari");
    q = j.question_add(game=g1, question="💐🌾");
    q = j.question_add(game=g1, question="Ⓜ️🐻");
    a = j.answer_add(question=q, answer="el mos");
    q = j.question_add(game=g1, question="🦄");
    a = j.answer_add(question=q, answer="Únic");
    q = j.question_add(game=g1, question="🚂");
    a = j.answer_add(question=q, answer="exprés"); 
    q = j.question_add(game=g1, question="🚂🐱🚬");
    a = j.answer_add(question=q, answer="exprés del gat cendrer");
    q = j.question_add(game=g1, question="🗝🌞");
    a = j.answer_add(question=q, answer="Clàudia");
    q = j.question_add(game=g1, question="👀🍾🍾");
    a = j.answer_add(question=q, answer="mirador caves");
    q = j.question_add(game=g1, question="💰❗️🥬");
    q = j.question_add(game=g1, question="🏠💬ℹ️");
    q = j.question_add(game=g1, question="🏠❄️❄️");
    a = j.answer_add(question=q, answer="fonda neus");
    q = j.question_add(game=g1, question="👅🤏🏪🚗");
    q = j.question_add(game=g1, question="🌉🇮🇹");
    a = j.answer_add(question=q, answer="pont romà");
    q = j.question_add(game=g1, question="            ");
    a = j.answer_add(question=q, answer="Sense nom");
    q = j.question_add(game=g1, question="📆🥂");
    q = j.question_add(game=g1, question="🔼");
    a = j.answer_add(question=q, answer="triangle");
    q = j.question_add(game=g1, question="🏠❓🧏🏻‍♀❓👉🏼");


    gs = j.game_list()
    for g in gs:
        print(str(g.name))
        for q in g.questions:
            print("q:"+str(q.name))
            for a in q.answers:
                print("a:"+str(a.name))
