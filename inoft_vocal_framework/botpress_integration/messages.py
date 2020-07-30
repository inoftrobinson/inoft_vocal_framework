from inoft_vocal_engine.inoft_vocal_framework.speechs.ssml_builder_core import Speech, SpeechsList

BUILTIN_TEXT_PSSHWG = SpeechsList("builtin_text-pSsHWg").speechs([
    Speech().add_text("""
👋, {{user.nickname}}!
""").set_prob(1),
    Speech().add_text("""
Hello, {{user.nickname}}!
""").set_prob(1),
    Speech().add_text("""
Welcome to Botpress, {{user.nickname}}!
""").set_prob(1),
])
BUILTIN_TEXT_AY5SSW = SpeechsList("builtin_text-AY5SSW").speechs([
    Speech().add_text("""
This is the first time we speak 🤖
""").set_prob(1),
])
BUILTIN_TEXT_BFSOMF = SpeechsList("builtin_text-bFsOmf").speechs([
    Speech().add_text("""
We already spoke {{temp.$r}} times!
""").set_prob(1),
])
BUILTIN_TEXT_TTZRCV = SpeechsList("builtin_text-TtzrCV").speechs([
    Speech().add_text("""
Alright, I have forgotten your name.
""").set_prob(1),
])
BUILTIN_TEXT_Z0J9QH = SpeechsList("builtin_text-z0J9qh").speechs([
    Speech().add_text("""
May I know your name please?
""").set_prob(1),
])
BUILTIN_TEXT_X069LE = SpeechsList("builtin_text-X069Le").speechs([
    Speech().add_text("""
Try saying something like "forget my name"!
""").set_prob(1),
])
BUILTIN_TEXT_KKQ8C3 = SpeechsList("builtin_text-kKQ8C3").speechs([
    Speech().add_text("""
(To see how this works, double-click anywhere on the flow and go to the "Transitions" panel)
""").set_prob(1),
])
BUILTIN_TEXT_LBS0RE = SpeechsList("builtin_text-lbs0Re").speechs([
    Speech().add_text("""
* Ambience...* *Enorme clairon, bruit de mouvement de tente, une personne gueulant dans le barrequement * C'est pas le jour pour dormir ! Réveiller-vous, j'attend tout le monde au centre du camp. Trois minutes, et que ça saute !
* Tu te lève et tu commence à t'habiller * * Willie * Hey Léo, bien dormi ?
""").set_prob(1),
])
BUILTIN_TEXT_SRXAPP = SpeechsList("builtin_text-sRxAPP").speechs([
    Speech().add_text("""
Bot Memory is used by the bot to store information about a conversation. Here's an example.
""").set_prob(1),
])
BUILTIN_TEXT_6RY1F5 = SpeechsList("builtin_text-6RY1f5").speechs([
    Speech().add_text("""
A bot could ask questions that are similar but have different meanings. To differentiate between the meanings of these questions, we use Contexts.
""").set_prob(1),
])
BUILTIN_TEXT_UP2OZM = SpeechsList("builtin_text-UP2ozm").speechs([
    Speech().add_text("""
Please pick an animal from the choices, I'm not a Zoologist.
""").set_prob(1),
])
BUILTIN_TEXT_LALV5X = SpeechsList("builtin_text-lALv5x").speechs([
    Speech().add_text("""
Please ask questions about that animal, like its life span or its habitat.
""").set_prob(1),
])
BUILTIN_TEXT_BOU5XW = SpeechsList("builtin_text-bOU5xw").speechs([
    Speech().add_text("""
Please refer to our [documentation](https://botpress.com/docs/build/memory) to learn more about Bot Memory.
""").set_prob(1),
])
BUILTIN_TEXT_SKQXXN = SpeechsList("builtin_text-SKQxXN").speechs([
    Speech().add_text("""
Ask me something thats included in the choices. Let's try again.
""").set_prob(1),
])
BUILTIN_TEXT_T8OA8M = SpeechsList("builtin_text-T8Oa8M").speechs([
    Speech().add_text("""
To learn more about how to setup a Contextual FAQ, please refer to our [tutorial](https://botpress.com/docs/tutorials/contextual-faq)
""").set_prob(1),
])
BUILTIN_TEXT_YFOIFD = SpeechsList("builtin_text-yFOIFD").speechs([
    Speech().add_text("""
Tell me if you need help!
""").set_prob(1),
])
BUILTIN_TEXT_ERROR = SpeechsList("builtin_text-error").speechs([
    Speech().add_text("""
😯 Oops! We've got a problem. Please try something else while we're fixing it 🔨
""").set_prob(1),
])
BUILTIN_TEXT_UT1TP5 = SpeechsList("builtin_text-uT1TP5").speechs([
    Speech().add_text("""
* Willie * Pareil, j'ai à peine dormi. T'était pareil lors de ton premier assignation ?
""").set_prob(1),
])
BUILTIN_TEXT__FWW96 = SpeechsList("builtin_text--FWw96").speechs([
    Speech().add_text("""
T'a de la chance. J'ai à peine dormi, t'était pareil lors de ton premier assignation ?
""").set_prob(1),
])
BUILTIN_TEXT_WQHTNB = SpeechsList("builtin_text-wqhtNB").speechs([
    Speech().add_text("""
* Willie * Ouai....* sigh* Bon de toute façon, c'est pour la nation, hein. Et surout, la ont plus vraiment le choix * laughing * C'est bon t'est prêt ?
""").set_prob(1),
])
BUILTIN_TEXT_VOCLDO = SpeechsList("builtin_text-VOcldO").speechs([
    Speech().add_text("""
Quoi ? Je suis vraiment mal réveillé. J'ai pas réussi à dormir, t'était pareil lors de ton premier assignation ?
""").set_prob(1),
])
BUILTIN_TEXT_GZ5LMT = SpeechsList("builtin_text-GZ5Lmt").speechs([
    Speech().add_text("""
* Willie * On vraiment pas le temps Léo, aller viens. ** walking ** Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
])
BUILTIN_TEXT_NIVD2C = SpeechsList("builtin_text-NiVD2C").speechs([
    Speech().add_text("""
* Willie * Ok super, allons-y. ** walking ** * Chef * Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
])
BUILTIN_TEXT_CLAWQ0 = SpeechsList("builtin_text-Clawq0").speechs([
    Speech().add_text("""
* Willie * De toute façon, faut qu'y aille. ** walking ** Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
])
BUILTIN_TEXT_LHJGU5 = SpeechsList("builtin_text-LHJgU5").speechs([
    Speech().add_text("""
* Chef * T'essais de faire le malin Major ?
""").set_prob(1),
])
BUILTIN_TEXT_0MCHOO = SpeechsList("builtin_text-0McHoo").speechs([
    Speech().add_text("""
Tu te fous de moi ?
""").set_prob(1),
])
BUILTIN_TEXT_AMLZRX = SpeechsList("builtin_text-aMlZRX").speechs([
    Speech().add_text("""
C'est bien ce que je croyait. ** Willie ** Léo, arrête de déconner ! Ok ?
""").set_prob(1),
])
BUILTIN_TEXT_GQUBNB = SpeechsList("builtin_text-gQuBnb").speechs([
    Speech().add_text("""
** gant te fouette * C'est pas le moment pour jouer au coup, reprend toi en main ! * Willie * Léo, soit sérieux ! Ok ?
""").set_prob(1),
])
BUILTIN_TEXT_DJKP2N = SpeechsList("builtin_text-dJKP2N").speechs([
    Speech().add_text("""
Vous jouerez Léo Major, éclaireur des forces canadiennes agé de toute juste 23 ans. Votre histoire commençeras durant la bataille de l'Escaut, qui c'est produite du 2 octobre jusqu'au 8 novembre 1944. 135 000 soldats canadien, français britannique, polandais, américain, belges, néérlendais, et norvègien sont opposé a 90 000 soldats allemands. Cette opération à comme objectif d'ouvrir une route de ravitaillement vers la ville belge d'Anvers, pour pouvoir ravitailler en armes, hommes et ressources les forces alliés dans tout le reste du nord-ouest de l'Europe. Nous commerons dans la matinné du 30 octobre. Cette histoire raconte des faits réels, les choix auxquelles vont serez confrontés, ont réelement vécu été vécu par Léo Major en 1944. Etes-vous prêt à jouer ?
""").set_prob(1),
])
BUILTIN_TEXT_MVDSF5 = SpeechsList("builtin_text-mvdSF5").speechs([
    Speech().add_text("""
* chef * Cela fait 28 jours que nous somme bloquer ici. Certains d'entre vous ne le savent pas encore, mais ces ordures de la Wehrmacht innonde et ont piégés tous les endroits pratiquables autour de la rivière. Plus de 10 000 hommes ont déjà été perdu à essayer ça, la moitié étais canadiens. Il nous faudrais des éclaireurs agile et chevronné, pour identifier les véhicules qu'ils utilisent pour transporter eau et munitions. Nous avons besoin de 2 personnes. Des volontaires ?
""").set_prob(1),
])
BUILTIN_TEXT_9JHDUX = SpeechsList("builtin_text-9jHdux").speechs([
    Speech().add_text("""
** Willie ** Léo et moi nous portons volontaire ! N'est-ce pas Léo ?
""").set_prob(1),
])
BUILTIN_TEXT_PODCGV = SpeechsList("builtin_text-podcGV").speechs([
    Speech().add_text("""
C'est décidé Major ! Je suppose que Arseneault t'accompagneras ? * Willy * Oui chef ! Vous partez dans H moin 30. * Charles * Oui chef ! ** bruit de pas qui s'en vont **
""").set_prob(1),
])
BUILTIN_TEXT_H7OF88 = SpeechsList("builtin_text-H7Of88").speechs([
    Speech().add_text("""
* chef * Très bien, c'est décidé. Vous partez dans H moins 30 minutes. Bonne chance. Oui chef ! ** Bruit de pas qui s'en vont **
""").set_prob(1),
])
BUILTIN_TEXT_XO49IE = SpeechsList("builtin_text-xo49ie").speechs([
    Speech().add_text("""
* Charles * ** tousse ** Oui chef !
""").set_prob(1),
])
BUILTIN_TEXT_YU8LDM = SpeechsList("builtin_text-yU8lDm").speechs([
    Speech().add_text("""
** marche en partant à deux ** 
""").set_prob(1),
])
BUILTIN_TEXT__XTGRB = SpeechsList("builtin_text-_xtGrB").speechs([
    Speech().add_text("""
Ok, Charles, notre position devrait être safe, ont peut faire une pause dans cette petite maison, les allemands sont à peut-être 15 killomètre. Sécurisons notre position avant tout. ** Narration/Menu ** Souhaitez-vous demander à Charles de sécurisé l'intérieur ou l'extérieur ?
""").set_prob(1),
])
BUILTIN_TEXT_PHCISY = SpeechsList("builtin_text-pHcIsy").speechs([
    Speech().add_text("""
** bruit de pas et de terre ** ** ouverture de vielle porte ** ** pas très len ** ** t'entend un bruit à l'extérieur avec de micros chuchottement ** ** pas continu à l'intérieur, il y à des petits craquements ** ** Enorme bruit de craquement **  ** Narration/menu ** Le bruit venais de derrière une porte devant vous. Vous pouvez ouvrir la porte ou tiré à travers avec votre fusil, que choissisez vous ?
""").set_prob(1),
])
BUILTIN_TEXT_0LKZRM = SpeechsList("builtin_text-0lkzRm").speechs([
    Speech().add_text("""
Vous devez choisir quel position vous demander à Charles de sécurisé. Intérieur ou l'extérieur ?
""").set_prob(1),
])
BUILTIN_TEXT_PFWE0A = SpeechsList("builtin_text-PFWe0a").speechs([
    Speech().add_text("""
Charles, tu peut sécurisé l'intérieur et je fais l'extérieur ? * Charles * Heeeeu en faites, l'intérieur me fait un peu peur, ça te dérangerais pas que je fasse l'extérieur ? Non ?
""").set_prob(1),
])
BUILTIN_TEXT_C_BCIN = SpeechsList("builtin_text-c_bcIn").speechs([
    Speech().add_text("""
Charles, je sécurise l'intérieur et tu fais l'extérieur, ça te vas ? * Charles * Ok super ! Tu me passe tes jumelles ? ** bruit d'équipement ** 
** bruit de pas et de terre ** ** ouverture de vielle porte ** ** pas très len ** ** t'entend un bruit à l'extérieur avec de micros chuchottement ** ** pas continu à l'intérieur, il y à des petits craquements ** ** Enorme bruit de craquement **  ** Narration/menu ** Le bruit venais de derrière une porte devant vous. Vous pouvez ouvrir la porte ou tiré à travers avec votre fusil, que choissisez vous ?
""").set_prob(1),
])
BUILTIN_TEXT_YYVCCP = SpeechsList("builtin_text-YYVcCp").speechs([
    Speech().add_text("""
* Charles * Merci beaucoup ! Tu peut me passer tes jumelles ? ** bruit d'équipement ** Merci, a tout de suite !
** bruit de pas et de terre ** ** ouverture de vielle porte ** ** pas très len ** ** t'entend un bruit à l'extérieur avec de micros chuchottement ** ** pas continu à l'intérieur, il y à des petits craquements ** ** Enorme bruit de craquement **  ** Narration/menu ** Le bruit venais de derrière une porte devant vous. Vous pouvez ouvrir la porte ou tiré à travers avec votre fusil, que choissisez vous ?
""").set_prob(1),
])
BUILTIN_TEXT_9R0F_I = SpeechsList("builtin_text-9R0F-i").speechs([
    Speech().add_text("""
Quand je disais un peu peur, en réalité ça me terrorise, vraiment je peut pas faire l'intérieur. Ca te derange pas à ce point que je fasse l'extérieur, non ?
""").set_prob(1),
])
BUILTIN_TEXT_BZGKZC = SpeechsList("builtin_text-BzGkZC").speechs([
    Speech().add_text("""
C'est vraiment pas sympa !! Charles * Je fais l'extérieur et c'est tout. * Leo * Ok, ok, fait l'extérieur. * Charles * Finalement ** ennuyé **, tu me passe tes jumelles ? ** bruit d'équipement ** * Charles * A tout de suite ** ennuyé **
** bruit de pas et de terre ** ** ouverture de vielle porte ** ** pas très len ** ** t'entend un bruit à l'extérieur avec de micros chuchottement ** ** pas continu à l'intérieur, il y à des petits craquements ** ** Enorme bruit de craquement **  ** Narration/menu ** Le bruit venais de derrière une porte devant vous. Vous pouvez ouvrir la porte ou tiré à travers avec votre fusil, que choissisez vous ?
""").set_prob(1),
])
BUILTIN_TEXT_RZN1IV = SpeechsList("builtin_text-RZn1IV").speechs([
    Speech().add_text("""
Vous devez choisir. Ouvrir la porte ou tirer à travars ?
""").set_prob(1),
])
BUILTIN_TEXT_XPYD6E = SpeechsList("builtin_text-XpyD6e").speechs([
    Speech().add_text("""
** ouverture de porte très rapide ** ** bruit de rats ** ** essouflement de relachement ** * Léo * Ouste, dégage. ** bruits de pas len derrière toi ** * Menu * Souhaiter-vous brandir votre fusil face au bruit derrière vous ?
""").set_prob(1),
])
BUILTIN_TEXT_KNFFLH = SpeechsList("builtin_text-KNffLH").speechs([
    Speech().add_text("""
** pan pan ** ** bruit ouverture de porte très rapide ** * Léo * C'est juste un rat... ** essouflement de relachement ** bruits de pas qui court derrière toi ** * Menu * Souhaiter-vous brandir votre fusil face au bruit derrière vous ?
""").set_prob(1),
])
BUILTIN_TEXT_ZJNFHM = SpeechsList("builtin_text-Zjnfhm").speechs([
    Speech().add_text("""
** Charles ** Wow, Léo c'est moi. Tout vas bien ?
""").set_prob(1),
])
BUILTIN_TEXT_63LMT3 = SpeechsList("builtin_text-63LMT3").speechs([
    Speech().add_text("""
* Charles * Léo, ça vas ? Tout vas bien ?
""").set_prob(1),
])
BUILTIN_TEXT_ALJWKS = SpeechsList("builtin_text-alJwKS").speechs([
    Speech().add_text("""
* Léo * C'était qu'un rat, t'inquiète pas. Tout est beau pour l'extérieur ? * Charles * Oui, c'est sécurisé. * Leo * Ok, t'as pris deux boites de conserve c'est ça ? * Charles * Oui, une pour chaque, voilà la tienne ! ** Menu ** Souhaitez vous prendre la boite, ou rationner ? 
""").set_prob(1),
])
BUILTIN_TEXT_SLI_QZ = SpeechsList("builtin_text-sLI_qz").speechs([
    Speech().add_text("""
** Menu ** Choissisez-vous de prendre la bôite ou de la rationner ?
""").set_prob(1),
])
BUILTIN_TEXT_UL3OIL = SpeechsList("builtin_text-UL3OiL").speechs([
    Speech().add_text("""
* Léo * Merci Charles. Dis, il y à pas d'étiquette, tu sais ce que c'est ? * Léo * Non, je sais juste que c'est pas vide. Si tu devais deviner, tu pense qu'il y aurais quoi dans ta converse ?
""").set_prob(1),
])
BUILTIN_TEXT_7ZWONR = SpeechsList("builtin_text-7ZWONR").speechs([
    Speech().add_text("""
** Léo ** Charles, en tant qu'éclaireur on doit économiser ce qu'ont as. Ont sais jamais pourquoi combien de temps ont seras dehors. * Charles * Tu dis ça après avoir juste une mission d'éclaireur ? ** Menu ** Allez-vous répondre à Charles de manière amusé ou sérieux ?
""").set_prob(1),
])
BUILTIN_TEXT_VAPRWA = SpeechsList("builtin_text-VaprwA").speechs([
    Speech().add_text("""
* Léo * La moyenne de missions pour un éclaireur c'est 3. ** ambience fond pendant 3 secondes ** * Charles * Mais il aurais pas fallu qu'ont prenne plus tout simplement ? * Léo * Ont auras du mal à courir avec 1 kilo de conserves sur le dos. * Léo * T'as raison... Ont peut en partager une alors ? Non ?
""").set_prob(1),
])
BUILTIN_TEXT_DSH9LV = SpeechsList("builtin_text-dSH9lV").speechs([
    Speech().add_text("""
Choissiez vous de lui répondre de manière sérieuse ou amusé ?
""").set_prob(1),
])
BUILTIN_TEXT_MO0AHG = SpeechsList("builtin_text-Mo0aHG").speechs([
    Speech().add_text("""
* Leo (amusé) * Sérieux, tu pense ça ? Ont vas voir ** double bruitage ouverture de conserve ** * Charles * J'ai des haricots, et toi Léo ? ** silence de deux secondes avec une ambiance ** * Léo dessus * Des haricots blancs... * Charles * Moi c'est des haricots verts ** silence de deux secondes ** ** Charles et Léo explosent de rire. ** rire s'éteind en quelques secondes **. * Charles * Tu les préfère chaud ou froid ?
""").set_prob(1),
])
BUILTIN_TEXT_JV7EI4 = SpeechsList("builtin_text-JV7Ei4").speechs([
    Speech().add_text("""
* Léo * Ok, prenons celle la. ** attrape conserve ** Dis, il y à pas d'étiquette, tu sais ce que c'est ? * Charles * Non, je sais juste que c'est pas vide. Si tu devais deviner, tu pense qu'il y a quoi dedans ?
""").set_prob(1),
])
BUILTIN_TEXT_MOQVIJ = SpeechsList("builtin_text-mOQVij").speechs([
    Speech().add_text("""
* Charles (amusé) * Tu préfère les haricots froids ? C'est fou en 10 ans, j'ai jamais soupsonné que tu les préfere froids ! Santé à nos bôites d'haricots ! ** boites se frappant ** * Charles (doucement) * C'est drôle, mais en faites les haricots c'est un peu comme les mineraix dans notre mine, non ?
""").set_prob(1),
])
BUILTIN_TEXT_DHM90O = SpeechsList("builtin_text-dHm90O").speechs([
    Speech().add_text("""
Chaud ou froid ? Sinon je choisi pour toi hein.
""").set_prob(1),
])
BUILTIN_TEXT_2RG9W6 = SpeechsList("builtin_text-2RG9W6").speechs([
    Speech().add_text("""
* Charles * Si tu te décide pas, faisons froid. Ce seras plus simple. TIens, voici tes haricots * Charles (doucement) * C'est drôle, mais en faites les haricots c'est un peu comme les mineraix dans notre mine, non ?
""").set_prob(1),
])
BUILTIN_TEXT_FLZSA3 = SpeechsList("builtin_text-FlZsA3").speechs([
    Speech().add_text("""
* Léo * La première est la plus riche. Je suis prêt, que c'est cette mission qui t'apprendras le plus parmis toute celle qu'ont feras. Ou même, regarde notre mine. Ont apprend tellement, ce seras bien plus simple pour notre deuxième, troisième et centième ! * Charles (avec un ton content) * T'as raison... ** silence de 1 seconde avec ambience ** D'ailleurs, vu que tu parle de première, ont peut se partager la première conserve, non ?
""").set_prob(1),
])
BUILTIN_TEXT_DWB0JL = SpeechsList("builtin_text-Dwb0Jl").speechs([
    Speech().add_text("""
* Charles * T'est sûr ? Après tout, si ont as besoin de courir il nous faudras des forces. * Léo * Bon... ok, mais seulement une. * Charles * Aaaaah, prenons celle la. ** attrape conserve ** * Léo * Dis, il y à pas d'étiquette, tu sais ce que c'est ? * Charles * Non, je sais juste que c'est pas vide. Si tu devais deviner, tu pense qu'il y a quoi dedans ?
""").set_prob(1),
])
BUILTIN_TEXT_EAVIRL = SpeechsList("builtin_text-EaVirl").speechs([
    Speech().add_text("""
* Charles * Ont vas voir ! C'est le grand moment... ** ouverture d'une boite de conserve ** ** silence de deux secondes ** * Léo * Alors ? ** Charles déçu * Des haricots verts, la classique... Mangeons les froids, ça vaut même pas le coup de les réchauffer. ** Menu ** Souhaitez-vous répondre à Charles avec emphatie ou ennuie ?
""").set_prob(1),
])
BUILTIN_TEXT_2WHX3R = SpeechsList("builtin_text-2WHX3r").speechs([
    Speech().add_text("""
Vous devez choisir de lui répondre avec empathie ou ennuie.
""").set_prob(1),
])
BUILTIN_TEXT_PSACNA = SpeechsList("builtin_text-PsacnA").speechs([
    Speech().add_text("""
* Charles (amusé) * Ca m'étonne pas de toi, toujours à choisir le chaud plutôt que le froid. T'a un briquet dans ton sac, tu pourrais me le passer ?
""").set_prob(1),
])
BUILTIN_TEXT_OZHJIL = SpeechsList("builtin_text-oZHjil").speechs([
    Speech().add_text("""
* Léo * Charles, ** ennuie dans la voix ** c'est pas facile pour moi non plus. Reprend toi en mains, si tu peste à propos du fait qu'ont mange quasiment que des haricots, tu nous rendras tous les deux vulnérables. * Charles * Je sais, je sais... C'est juste tellement stupide cette guerre, ça fait déjà plus d'un an que ça dure, et ont nous dis que ça vas duré encore 2 à 3 mois, j'en ai assez... Pas toi ?
""").set_prob(1),
])
BUILTIN_TEXT_M9BFMB = SpeechsList("builtin_text-M9BFMB").speechs([
    Speech().add_text("""
* Léo * Il doit y avoir des raisons de pourquoi la guerre dure aussi longtemps, et pourquoi se reconcilier est pas si simple. Des fois, la confrontation est la solution. * Charles (ennuyé) * Et pourtant, est-ce que pour notre mine ont à eu besoin d'utiliser la force ? * Léo (amusé) * Et pourtant notre mine nous à mis dans plus de dette que de richesses... * Charles (légèrement ennuyé mais curieux * Tu pense qu'utiliser la force aurait pu nous aider ? Sois honnete...
""").set_prob(1),
])
BUILTIN_TEXT_9F_TKH = SpeechsList("builtin_text-9f_TKH").speechs([
    Speech().add_text("""
* Léo * T'as raison, il y à peut-être même pas de réponse approprié...  ** amusé et géné ** Ca te dit ont parle d'autre chose ? 
""").set_prob(1),
])
BUILTIN_TEXT_7SQ25X = SpeechsList("builtin_text-7sQ25x").speechs([
    Speech().add_text("""
* Charles * T'as pas besoin d'une excuse si tu les préfère froid ! * Léo * Ok, ok, je vais le chercher ** fouiller dans un sac pendant plusieurs secondes ** Tu vas rire. * Charles * T'est sérieux ? * Léo * Oui. * Charles * Froid ? * Léo (pas très fier) * Froid... ** ils commencent à manger ** C'est pas aussi drôle que le briquet, mais je viens de me dire, qu'en faites les haricots c'est un peu comme les mineraix dans notre mine, non ?
""").set_prob(1),
])
BUILTIN_TEXT_X6L9AV = SpeechsList("builtin_text-x6L9aV").speechs([
    Speech().add_text("""
Je vais te le chercher ** fouiller dans un sac pendant plusieurs secondes ** Tu vas rire. * Charles * T'est sérieux ? * Léo * Oui. * Charles * Froid ? * Léo (pas très fier) * Froid... ** ils commencent à manger ** C'est pas aussi drôle que le briquet, mais je viens de me dire, qu'en faites les haricots c'est un peu comme les mineraix dans notre mine, non ?
""").set_prob(1),
])
BUILTIN_TEXT_DQURAC = SpeechsList("builtin_text-dQuRac").speechs([
    Speech().add_text("""
* Charles * Ben oui, la première conserve d'haricots depuis 1 mois est toujours meilleur que la 15 ème du mois, pas vrai ?
""").set_prob(1),
])
BUILTIN_TEXT_CFEKGJ = SpeechsList("builtin_text-cFekgJ").speechs([
    Speech().add_text("""
* Léo * C'est ça. Alors que pourtant les haricots sont toujours les mêmes, prenne le même temps à être cultivé, lavés, mis en boites et transporter. Au fur et à mesure, les haricots deviennent moins important, mais les terrains, les batiments et les engrais prenne de l'importance. Tu commence à comprendre ce que j'ai en tête ?
""").set_prob(1),
])
BUILTIN_TEXT_W5BIYZ = SpeechsList("builtin_text-W5bIyZ").speechs([
    Speech().add_text("""
* Charles * Les haricots sont comme le fer de notre mine. Chaque nouveau kilo deviens  moins intérréssant, mais ce qui vas le devenir c'est d'imaginer et de crée ensemble les façons pour pouvoir récolter plus de minéraix à meilleurs coûts ! ** petit silence ** ** en rigolant * J'ai l'air bon pour l'asile à parler d'engrais et de fer, non ?
""").set_prob(1),
])
BUILTIN_TEXT_NNMARE = SpeechsList("builtin_text-nNmAre").speechs([
    Speech().add_text("""
* Charles * Hey ! J'attendais pas que tu dise oui à ça ! C'est pas sympa ! ** les deux rigole **. Enfin, j'ai reçu une lettre à propos de l'emprunt de la mine, ça te dit qu'on en discute maintenant ?
""").set_prob(1),
])
BUILTIN_TEXT_JC5NXV = SpeechsList("builtin_text-jC5nXV").speechs([
    Speech().add_text("""
* Charles * Ahah ** arrête de rigoler petit à petit **, je compte pas y aller avant d'être vieux et d'avoir des enfants et petits enfants. Enfin... ** petit 'mélancolie' ? **. D'ailleurs, ** un peu attristé et ennuyé ** j'ai reçu une lettre à propos de l'emprunt de la mine, ça te dit qu'on en discute maintenant ?
""").set_prob(1),
])
BUILTIN_TEXT_1VIQJ4 = SpeechsList("builtin_text-1ViQJ4").speechs([
    Speech().add_text("""
* Charles * Y à pas un meilleur moment que maintenant, comme tu dis, ont sais jamais si ont vas avoir le temps. Ont peut en parler maintenant, s'il te plait ?
""").set_prob(1),
])
BUILTIN_TEXT_2QQDDL = SpeechsList("builtin_text-2QQdDl").speechs([
    Speech().add_text("""
Section sur la dette de la mine, pour comprendre l'importance que ça à, et les difficultés financières que la guerre ont crée pour Léo et Charles
""").set_prob(1),
])
BUILTIN_TEXT_MAPR9O = SpeechsList("builtin_text-MApR9O").speechs([
    Speech().add_text("""
* chef * C'est bien ce que je pensais... ** silence de deux secondes et le chef s'éloigne ** Soldats ! Cela fait 28 jours que nous somme bloquer ici. Certains d'entre vous ne le savent pas encore, mais ces ordures de la Wehrmacht innonde et ont piégés tous les endroits pratiquables autour de la rivière. Plus de 10 000 hommes ont déjà été perdu à essayer ça, la moitié étais canadiens. Il nous faudrais des éclaireurs agile et chevronné, pour identifier les véhicules qu'ils utilisent pour transporter eau et munitions. Nous avons besoin de 2 personnes. Des volontaires ?
""").set_prob(1),
])
BUILTIN_TEXT_ZDOKTC = SpeechsList("builtin_text-ZDokTc").speechs([
    Speech().add_text("""
*Léo* Très bien Willie, j'ai pris des jumelles et la radio, tu à pris la carte et quelques trucs ravitaillements ? *Willie* Oui, donc il ne nous reste plus qu'à prendre des armes ? *Luc* C'est ça, allons voir le l'aumonier. *Pas* *Bruit d'hommes qui parle augmentant petit à petit*  * Luc * Major, Arsenault ! Que puis-je faire pour vous ? Vous venez chercher de l'équipement ? 
""").set_prob(1),
])
BUILTIN_TEXT_BURO1C = SpeechsList("builtin_text-bUro1C").speechs([
    Speech().add_text("""

""").set_prob(1),
])
BUILTIN_TEXT_5HOCPF = SpeechsList("builtin_text-5hocpF").speechs([
    Speech().add_text("""

""").set_prob(1),
])
BUILTIN_TEXT_GDQOHR = SpeechsList("builtin_text-GDqoHr").speechs([
    Speech().add_text("""

""").set_prob(1),
])
BUILTIN_TEXT_XSNW_U = SpeechsList("builtin_text-xsnw_u").speechs([
    Speech().add_text("""
* Luc * Ca m'étonnerais vu l'heure que vous soyez venu pour discuter gonzesses. Je suppose que vous partez pour une mission, c'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_HH2NQ5 = SpeechsList("builtin_text-hh2NQ5").speechs([
    Speech().add_text("""
* Luc * Ok ! Vu l'heure, je suppose que vous partez en mission ? C'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_VH1ZDV = SpeechsList("builtin_text-vh1zdV").speechs([
    Speech().add_text("""
* Luc * Toujours fidèle à toi même ! C'est une mission secrète, pas vrai ?
""").set_prob(1),
])
BUILTIN_TEXT_9XLAKD = SpeechsList("builtin_text-9XLAKD").speechs([
    Speech().add_text("""
* Luc * Par tout hasard... Cette mission secrète elle implique des demoiselles ?
""").set_prob(1),
])
BUILTIN_TEXT_W0BPZF = SpeechsList("builtin_text-w0BpZF").speechs([
    Speech().add_text("""
Peu importe, vous êtes combien ? T'a besoin d'équipements pour combien de personnes ?
""").set_prob(1),
])
BUILTIN_TEXT_CMIXBA = SpeechsList("builtin_text-cmiXba").speechs([
    Speech().add_text("""
* Luc * Héhé, faudras que vous me racontier tous les deux. Et en faites pour cette mission "secrète", vous avez besoin d'équipement pour combien de personnes ?
""").set_prob(1),
])
BUILTIN_TEXT_P6DAJE = SpeechsList("builtin_text-P6DaJE").speechs([
    Speech().add_text("""
* Luc * Toujours la même chose alors... ** silence d'une seconde ** Bon en faites pour cette mission, t'a besoin d'équipement pour combien de personnes ?
""").set_prob(1),
])
BUILTIN_TEXT_M85FOA = SpeechsList("builtin_text-m85Foa").speechs([
    Speech().add_text("""
*Luc* C'est pas grave si tu veut pas me donner les détails. Ont se dis que c'est une mission de routine ?
""").set_prob(1),
])
BUILTIN_TEXT_GEEC4H = SpeechsList("builtin_text-GEEC4H").speechs([
    Speech().add_text("""
* Luc * ** enervé ** Arrête de nous faire perdre du temps, ont sais tous les deux qu'à cette heure, si c'est pas une mission spécial, c'est pour de la reconnaissance. Vous avez besoin d'équiments pour combien de personnes ?
""").set_prob(1),
])
BUILTIN_TEXT_YWSRMC = SpeechsList("builtin_text-ywSRmC").speechs([
    Speech().add_text("""
* Luc * Ah bah voila !! * silence de 1 seconde * Bon, au final vous besoin d'équipement pour combien de personnes ?
""").set_prob(1),
])
BUILTIN_TEXT_2I2WB4 = SpeechsList("builtin_text-2i2WB4").speechs([
    Speech().add_text("""
* Luc * T'est sûr ? * Léo * Non, je déconnais. C'est juste que des fois je suis super con et j'adore faire chier les gens. Genre je kiffe en particulier faire chier les gens qui écrivent des histoires, tu voit ce que je veut dire ? * Luc * Totalement, c'est tellement drôle. * Léo * Bon en faites j'ai besoin d'équipements pour deux personnes.
""").set_prob(1),
])
BUILTIN_TEXT_9X2NQK = SpeechsList("builtin_text-9x2nqk").speechs([
    Speech().add_text("""
* Luc * De base j'aurais parié que vous seriez que tous les deux. C'est ça non ?
""").set_prob(1),
])
BUILTIN_TEXT_B7RMGS = SpeechsList("builtin_text-B7RMgs").speechs([
    Speech().add_text("""
* Luc * Classique, comme la guerre. Il y à juste vous deux je suppose, c'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_CBPJNX = SpeechsList("builtin_text-cbpjnx").speechs([
    Speech().add_text("""
* Luc * Un peu comme toi, j'adorais faire de la reconnaissance. ** petite joie ** Il y à quoi, un an, j'étais dans la première division d'infantrie, je m'en rappelle comme si c'était hier. L'an dernier le 19 décembre, ont étais en Italie, à Ortana, tu connais ?
""").set_prob(1),
])
BUILTIN_TEXT_RNZGHM = SpeechsList("builtin_text-RnZgHm").speechs([
    Speech().add_text("""
* Léo * Ani ? * Luc * Ani Godfrey. Peut-être la femme la plus brave que j'ai jamais rencontré. Quasiment à faire peur tu voit. Elle à tuer plus de nazis que tous les soldats que je connais, combiné ! Elle battais n'importe qui au bras de fer. Et pourtant, c'éait fou elle avais pas l'air ! Même quand elle étais en tenu de camouflage, je peut te dire que dans le camp elle étais pas si bien camouflé ! Et sans ça tenu, je te dit pas hein, héhé. * silence d'une seconde * Elle devais même recevoir une médialle d'honneur, t'imagine ? Une femme recevoir une telle médiale, ça aurait changer tellement de choses. * Menu * Souhaitez-vous demander à Luc si elle à reçu la médaille ?
""").set_prob(1),
])
BUILTIN_TEXT_XPA8QX = SpeechsList("builtin_text-xPA8qX").speechs([
    Speech().add_text("""
* Léo * Elle à reçu la médaille ? * Luc * J'y viens ! 
""").set_prob(1),
])
BUILTIN_TEXT_LI_7KX = SpeechsList("builtin_text-Li_7Kx").speechs([
    Speech().add_text("""
C'est une petite ville d'Italie, elle étais dans les mains des nazis, ont nous avais dis que c'était important de la récuperer parce que c'était la seul ville juste à coté d'eau profondes où les gros bateaux de ravitaillement allier pourrais venir. C'est toujours logique quand ça viens du haut, mais quand t'est en bas, tu peut que flipper à attaquer une ville rempli de Nazi. Enfin sauf Ani... * Menu * Souhaitez-vous demander à Luc qui est Ani ?
""").set_prob(1),
])
BUILTIN_TEXT_4H2MTU = SpeechsList("builtin_text-4H2mtu").speechs([
    Speech().add_text("""
Juste toi et Willie, c'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_G7TMWJ = SpeechsList("builtin_text-g7TmwJ").speechs([
    Speech().add_text("""
* Luc * Ok, je pense que j'ai ce qui vas vous convenir, on commence par toi Léo ou par Willie ?
""").set_prob(1),
])
BUILTIN_TEXT_MIBBFS = SpeechsList("builtin_text-MiBbfs").speechs([
    Speech().add_text("""
* Luc * Si tu l'as utiliser, tu devrais connais déjà sa fiabilité et ses avantages. C'était il y à longtemps ? Si tu veut je peut te rappeller de ses avantages ? Oui ?
""").set_prob(1),
])
BUILTIN_TEXT_ZHTAW1 = SpeechsList("builtin_text-Zhtaw1").speechs([
    Speech().add_text("""
*Luc* Il est simple, fiable et puissant. Tu recharge plus lentement qu'avec un M1 Garrant, cependant tu a une bien meilleur précision. Théoriquement tu peut toucher un nazi jusqu'à 1 kilométre de distance, j'ai même une lunette qui est de coté, si tu prend le fusil, je te le passe, elle seras plus utile avec toi que dans mes caisses. Et si tu cherche quelque chose de plus corps à corps, j"ai autre chose en stock. Tu veut que je te montre ?
""").set_prob(1),
])
BUILTIN_TEXT_LX33H9 = SpeechsList("builtin_text-LX33h9").speechs([
    Speech().add_text("""
*Luc* J'ai vraiment pas mieux en stock. Ont se dit que tu pars sur le Lee Enfields ?
""").set_prob(1),
])
BUILTIN_TEXT_IFLIAH = SpeechsList("builtin_text-ifliAH").speechs([
    Speech().add_text("""
*Luc* Ok, c'est toi qui décide ! Je t'ai aussi sortis une autre arme si t'as besoin de quelque chose à plus courte distance ? Tu veut que je te la montre ?
""").set_prob(1),
])
BUILTIN_TEXT_8EYUCP = SpeechsList("builtin_text-8eyucp").speechs([
    Speech().add_text("""
Me dit pas que tu vas pas prendre de fusil ?
""").set_prob(1),
])
BUILTIN_TEXT_NVNHUV = SpeechsList("builtin_text-NVnhUV").speechs([
    Speech().add_text("""
* Luc * ** souffle pas content ** Comme tu veut... Tu vas au moins prendre un pistolet ?
""").set_prob(1),
])
BUILTIN_TEXT_GJL_UL = SpeechsList("builtin_text-Gjl_uL").speechs([
    Speech().add_text("""
*Luc* Tu veut mourrir ou quoi ? Prend un pistolet, s'il te plait dis moi oui pas non !
""").set_prob(1),
])
BUILTIN_TEXT_BFZB1M = SpeechsList("builtin_text-bfzb1m").speechs([
    Speech().add_text("""
*Luc* *enervé* Tu veut te faire tuer ou quoi ? *souffle en profondeur* Excuse moi Léo, ça ma juste tellement surpris. Je te fait confiance, si tu veut ne pas prendre d'arme, c'est toi qui choisis.
""").set_prob(1),
])
BUILTIN_TEXT_8HFKWY = SpeechsList("builtin_text-8hfKWY").speechs([
    Speech().add_text("""
*Luc* Ok, voyons pour Willie. Il sait toujours aussi mal visé je suppose ?
""").set_prob(1),
])
BUILTIN_TEXT_5S3T0_ = SpeechsList("builtin_text-5s3t0-").speechs([
    Speech().add_text("""
*Luc* *pose une arme relativement lourde* J'ai une Thompson M1921.
""").set_prob(1),
])
BUILTIN_TEXT_P2E4QQ = SpeechsList("builtin_text-P2E4Qq").speechs([
    Speech().add_text("""
*Luc* Elle est relativement légère pour son nombre de balles. Elle à un mode semi automatique mais c'est son mode automatique qui l'a fait briller. Par contre, beaucoup font la confusion, c'est pas une mitrailleuse, même si tu possède un chargeur de cent balles. Ca te donne de bonnes chances si il y à deux ou trois nazis armés en face de toi. ** petit silence d'une demi seconde ** Donc, qu'est-ce que tu compte prendre, le fusil ou la Thompson ?
""").set_prob(1),
])
BUILTIN_TEXT_YLIZXR = SpeechsList("builtin_text-YlIzxr").speechs([
    Speech().add_text("""
*Luc* Ca m'aurait étonné que tu connaisse pas déjà les détails. Alors, tu pars sur le fusil ou sur la Thompson ?
""").set_prob(1),
])
BUILTIN_TEXT_BP53AC = SpeechsList("builtin_text-Bp53AC").speechs([
    Speech().add_text("""
*Luc* Alors ? J'ai vraiment pas mieux. Tu prend la Thompson, le fusil, ou rien du tout ?
""").set_prob(1),
])
BUILTIN_TEXT_9E8F4U = SpeechsList("builtin_text-9e8F4u").speechs([
    Speech().add_text("""
*Luc* Comme tu veut, ont pars sur rien. Tu prend au moins un pistolet ?
""").set_prob(1),
])
BUILTIN_TEXT_ZP4HHJ = SpeechsList("builtin_text-Zp4HhJ").speechs([
    Speech().add_text("""
*Luc* Ouf, je croyais que t'avais perdu la tête.
""").set_prob(1),
])
BUILTIN_TEXT_KWM6JG = SpeechsList("builtin_text-KWM6Jg").speechs([
    Speech().add_text("""
*Luc* *pose un pistolet de manière très délicate sur la table* Un Colt M1911, c'est le pistolet semi-automatique standart. Il est pas que mauvais, tu veut que je te dise ce que j'en pense ?
""").set_prob(1),
])
BUILTIN_TEXT_NGYXJZ = SpeechsList("builtin_text-nGyXJz").speechs([
    Speech().add_text("""
*Luc* Théoriquement, c'est supposé être le meilleur pistolet, il est léger avec moins d'un kilo trois. Le modèle principale à des chargeurs de 7 balles, ça tire très vite et ça se recharge rapidement. Mais ce dont personne parle c'est son manque de puissance, tu vois une balle traverseras pas un bon casque sauf si t'est super proche. C'est le classique, si tu veut je peut également t'en montré un très différent. Je te le montre ?
""").set_prob(1),
])
BUILTIN_TEXT_K2XS_X = SpeechsList("builtin_text-K2XS-X").speechs([
    Speech().add_text("""
*Luc* *pose un pistolet sur la table* Un Webley Mk-5 *soupir content*, ça à 6 balles comparé au 7 du M1911, ça tire plus lentement, et c'est plus long à recharger. Mais ça à tellement pluis de puissance. Une balle peut passer à travers n'importe quelles caisse. Etonnamment, c'est utile plus souvent qu'ont ne le pense. Par contre, la sécurité est quasi inexistante. Pour toi, bien sûr j'aurais pas de soucis à te le conseiller. T'en pense quoi ? Tu prend le Colt ou le Webley ?
""").set_prob(1),
])
BUILTIN_TEXT_GGRNPY = SpeechsList("builtin_text-GgRnPy").speechs([
    Speech().add_text("""
c'est le modèle que j'avais utilisé en décembre dernier en Italie.
""").set_prob(1),
])
BUILTIN_TEXT_PSIKLE = SpeechsList("builtin_text-PsiKLE").speechs([
    Speech().add_text("""
*Luc* Ok, et en pistolets, tu veut que je t'en montre ?
""").set_prob(1),
])
BUILTIN_TEXT_RSNBPG = SpeechsList("builtin_text-rSNbPg").speechs([
    Speech().add_text("""
*Luc* Donc tu veut prendre le Colt ?
""").set_prob(1),
])
BUILTIN_TEXT_A7TOU4 = SpeechsList("builtin_text-A7ToU4").speechs([
    Speech().add_text("""
*Luc* *un peu ennuyé* Dis-moi, tu veut le premier qui est le Colt ou le deuxième le Webley ? *petit rire* Sinon tu peut rien prendre hein.
""").set_prob(1),
])
BUILTIN_TEXT__QGWUF = SpeechsList("builtin_text-_qGwUf").speechs([
    Speech().add_text("""
*Luc* Ok, parfait ! Ca me fait super plaisir que même si t'est jeune, tu prenne une arme classique !
""").set_prob(1),
])
BUILTIN_TEXT__QPGCU = SpeechsList("builtin_text--QPGcu").speechs([
    Speech().add_text("""
*Luc* Me dis pas que tu veut pas prendre de pistolet du tout. Si ?
""").set_prob(1),
])
BUILTIN_TEXT_MVUC4A = SpeechsList("builtin_text-Mvuc4A").speechs([
    Speech().add_text("""
*Luc* Ok pas de soucis, comme tu prend une autre arme, un pistolet n'est pas essentiel.
""").set_prob(1),
])
BUILTIN_TEXT_I3GXVQ = SpeechsList("builtin_text-i3GxvQ").speechs([
    Speech().add_text("""
*Luc* *avec une petite rage* C'était une blague ! T'as perdu la tête ? T'as ni pris le Lee Enfields, ni la Thompson, et maintenant tu vas pas prendre de pistolet ?! *silence d'une seconde* *plus calmement* Je te fais confiance, mais t'est vraiment sûr de rien vouloir prendre pour toi ?
""").set_prob(1),
])
BUILTIN_TEXT_VW2TQR = SpeechsList("builtin_text-vW2tqR").speechs([
    Speech().add_text("""
*Luc* Ok, ça m'étonne pas que tu connaisse déjà l'arme. J'en ai également un second pistolet très différent, tu veut que je te le montre ?
""").set_prob(1),
])
BUILTIN_TEXT_WWR0VE = SpeechsList("builtin_text-WWr0ve").speechs([
    Speech().add_text("""
*Luc* Ok Léo, ont commence par toi, alors...
""").set_prob(1),
])
BUILTIN_TEXT_8RRKTF = SpeechsList("builtin_text-8RrkTf").speechs([
    Speech().add_text("""
*Luc* Alors, c'est pas compliqué Léo. Ont commence par toi ou par Willie ?
""").set_prob(1),
])
BUILTIN_TEXT_UFHEEC = SpeechsList("builtin_text-UfHEEC").speechs([
    Speech().add_text("""
*Luc* T'inquiète pas, je comprend que vous poussiez pas réveler les détails. Assumons que "théoriquement" c'est pour toi et Willie.
""").set_prob(1),
])
BUILTIN_TEXT_KJWU5Q = SpeechsList("builtin_text-KjWu5q").speechs([
    Speech().add_text("""
*Luc* Ok ! Ont pars sur la Thompson.
""").set_prob(1),
])
BUILTIN_TEXT_RWXHVL = SpeechsList("builtin_text-RwXhVl").speechs([
    Speech().add_text("""
*Luc* Parfait, ont pars sur le Lee Enfields, j'aurais fait le même choix ! Je te fourni la lunette de visée.
""").set_prob(1),
])
BUILTIN_TEXT_PWRVAK = SpeechsList("builtin_text-pwRvaK").speechs([
    Speech().add_text("""
*Luc* Ok, tu m'as fait peur pendant une seconde, je croyais que tu n'allais pas prendre d'arme. Alors... *attrape un pistolet*
""").set_prob(1),
])
BUILTIN_TEXT_9_V_OC = SpeechsList("builtin_text-9-V-OC").speechs([
    Speech().add_text("""
*Luc* Alors maintenant en terme de munitions, et de kit de premiers secours, les ravitaillements sont pas encore arrivé, j'ai reçu l'ordre d'en donner qu'un de deux pour chaque mission. *Willie* Luc, c'est ridicule ! *Luc* Willie, les ordres sont les ordres, ont ne peut passé outre. *Willie* Il y a peu de gens qui en reviennent de là bas, ils nous faut toutes nos chances ! *Luc* C'est les ordres Willie, ont doit d'abord penser à ceux blesser aux camps, plutôt que ceux qui sont déjà condamnée ! *Menu* Souhaitez-vous prendre le coté de Willie ou de Luc ?
""").set_prob(1),
])
BUILTIN_TEXT_4JO_6P = SpeechsList("builtin_text-4jO_6p").speechs([
    Speech().add_text("""
*Luc* Tout est bon pour toi Léo ? Ont passe à Willie ?
""").set_prob(1),
])
BUILTIN_TEXT_JPSUIH = SpeechsList("builtin_text-JPSUIh").speechs([
    Speech().add_text("""
*Léo* Luc ! Tu peut faire une exception, personne ne le sauras ! *Luc* La question c'est pas si quelqu'un le ferras, mais que les autres aurons également moins de chances de s'en sortir. Si vous vous étiez déjà battu avec le dos d'un fusil, sans muniton, et avec des balles dans les jambes, vous comprendriez. Mais je suppose que vous avez jamais vécu ça ?
""").set_prob(1),
])
BUILTIN_TEXT_E8IE2J = SpeechsList("builtin_text-e8ie2J").speechs([
    Speech().add_text("""
*Luc* *énervé* Vous avez jamais vécu d'être face à une autre personne, qui comme vous, sa seul chance de survie est de vous tuer avec tout ce qu'il peut trouver. Vous avez jamais dù regarder quelqu'un dans les yeux pendant qu'il meurs de votre main de la pire des façons, et qu'il comprend qu'il reverras jamais sa famille. Ca à rien à voir avec tué quelqu'un avec une arme à feu. Si ça vous étais arrivé, vous seriez suffisamment respectué pour pas vouloir tout prendre, mais vouloir épargner à un maximum de personnes de vivre ça. *Très énervé* Désormais, vous prenez des munitions OU des soins de secours ?
""").set_prob(1),
])
BUILTIN_TEXT_KUJFK_ = SpeechsList("builtin_text-KUjfk_").speechs([
    Speech().add_text("""
*Luc* Vous voulez pas choisir ? Je vous ai choquer avec mon histoire ou quoi ? Vous prenez quoi au final ? Munitions ou kit de premier soins ?
""").set_prob(1),
])
BUILTIN_TEXT_WL84Z8 = SpeechsList("builtin_text-wl84z8").speechs([
    Speech().add_text("""
*Luc* *enevé* Si vous voulez pas choisir, je choisi pour vous, aller prenez les munitions.
""").set_prob(1),
])
BUILTIN_TEXT_D5PWFZ = SpeechsList("builtin_text-d5PWFZ").speechs([
    Speech().add_text("""
*Léo* Willie, si il y à des ordres ça doit parce qu'il y à vraiment plus beaucoup d'équipement. Soyons pas des cons avec un raisonnement égoiste, prenons l'un des deux ok ? *Willie* *énervé mais ce calme* Ok, je suis désolé, je me suis emporté *Luc* Pas de soucis Willie, ça arrive...
""").set_prob(1),
])
BUILTIN_TEXT_1I5JRP = SpeechsList("builtin_text-1I5JRP").speechs([
    Speech().add_text("""
Vous voulez prendre quoi ? Munitions ou kit de premier soins ? Sinon dis moi que tu sais pas, et je peut décider pour toi.
""").set_prob(1),
])
BUILTIN_TEXT_XXXQV6 = SpeechsList("builtin_text-xxXQV6").speechs([
    Speech().add_text("""
*Luc* Pas de soucis, c'est toujours difficile de choisir. Si j'étais vous je prendrais les munitions, si ça se passe bien, vous devriez pas vous retrouver à proximité d'ennemis, cependant les munitions à proximité ou à distance, sont toujours utile.
""").set_prob(1),
])
BUILTIN_TEXT_CT9H_C = SpeechsList("builtin_text-CT9H-C").speechs([
    Speech().add_text("""
*Luc* *énervé* Je vous parle pas d'après une bataille quand le résultat est défini !
""").set_prob(1),
])
BUILTIN_TEXT_8KVRJN = SpeechsList("builtin_text-8kvRjn").speechs([
    Speech().add_text("""
*Luc* *énervé* C'est bien ce que je croyais !
""").set_prob(1),
])
BUILTIN_TEXT_GBDFCV = SpeechsList("builtin_text-gBdFcV").speechs([
    Speech().add_text("""
*Léo* J'ai pas envie de prendre un coté, Willie, peu importe ce qu'ont en pense, ont à pas le droit de ne pas respecter des ordres. *Willie* *énervé mais ce calme* Souffle fort en ce calmant. *Luc* Léo à raison Willie, si je pouvais je vous donnerais les deux, mais les ordres ne sont pas là pour rien.
""").set_prob(1),
])
BUILTIN_TEXT_8PI4BX = SpeechsList("builtin_text-8Pi4bx").speechs([
    Speech().add_text("""
*Luc* *normalement et calmement* Donc vous voulez prendre quoi ? Des munitions ou un kit de premiers soins ? 
""").set_prob(1),
])
BUILTIN_TEXT_0ZW0TD = SpeechsList("builtin_text-0zw0Td").speechs([
    Speech().add_text("""
*Willie* *cherche dans son sac* Léo, je trouve pas la carte, c'est toi qui l'a pris ?
""").set_prob(1),
])
BUILTIN_TEXT_ZBXIL4 = SpeechsList("builtin_text-zbxiL4").speechs([
    Speech().add_text("""
*Léo* Oui, je l'ai dans ma poche, la voilà. *bruit de papier, passe la carte*
""").set_prob(1),
])
BUILTIN_TEXT_QKKTAJ = SpeechsList("builtin_text-QKKtaj").speechs([
    Speech().add_text("""
*Léo* C'est toi qui doit l'avoir Willie. *Willie* *continue à chercher* T'as raison, elle étais dans mon sac !
""").set_prob(1),
])
BUILTIN_TEXT_8X4ZC1 = SpeechsList("builtin_text-8X4Zc1").speechs([
    Speech().add_text("""
*Willie* Ok, alors, ont doit aller au nord, ont à deux chemins qui ont été sécurisé, un à l'ouest et l'autre à l'est. Tu veut jeter un coup d'oeil à la carte ?
""").set_prob(1),
])
BUILTIN_TEXT_HDEVHM = SpeechsList("builtin_text-hdeVhm").speechs([
    Speech().add_text("""
*Willie* Je pense que ce serais important qu'ont décide ensemble. T'est sûr que tu veut pas jeter un coup d'oeil ?
""").set_prob(1),
])
BUILTIN_TEXT_TLNYEQ = SpeechsList("builtin_text-tLNYEQ").speechs([
    Speech().add_text("""
*Luc* *s'assoire à coté de Willie* *Willie* Alors, ont à le choix entre passer par l'est, qui à été sécurisé il y à deux semaines et prendras 16 kilomètres de marche, car ont doit contourner cette petite rivière. Sinon ont peut prendre l'ouest, qui à été sécurisé depuis 4 jours, et qui nous prendras que 11 kilomètres. T'en pense quoi ? *Menu* Avant de prendre votre décision, voulez-vous prendre le temps de discuter avec Willie pour essayer de trouver un meilleur chemin ?
""").set_prob(1),
])
BUILTIN_TEXT_WP7E2U = SpeechsList("builtin_text-Wp7E2u").speechs([
    Speech().add_text("""
*Willie* Ok..., *un peu ennuyé*. En attendant que je choissises, je suis pas sûr de si j'ai pris mes jumelles, tu pourrais vérifier dans mon sac si je les ai prise ?
""").set_prob(1),
])
BUILTIN_TEXT_BTJLII = SpeechsList("builtin_text-bTJLii").speechs([
    Speech().add_text("""
*Willie* Tu veut pas regarder la carte, ou vérifier pour les jumelles, tu déprime ou quoi ?
""").set_prob(1),
])
BUILTIN_TEXT_I0AU78 = SpeechsList("builtin_text-I0Au78").speechs([
    Speech().add_text("""
*Willie* Attend... *silence d'une seconde* Ah, j'ai pas entendu ce que t'as dis.
""").set_prob(1),
])
BUILTIN_TEXT_8XDIBP = SpeechsList("builtin_text-8xDibP").speechs([
    Speech().add_text("""
*Léo* *bruit de pas, cherche dans un sac* Oui tu les as bien prise. *Willie* Ah ouf.
""").set_prob(1),
])
BUILTIN_TEXT_VIKJGQ = SpeechsList("builtin_text-VikJGQ").speechs([
    Speech().add_text("""
*Willie* Et c'est bon j'ai décidé, je pense que prendre l'ouest est mieux, car si ont à des soucis sur la route, ont pourras revenir plus rapidement. Ca te vas ?
""").set_prob(1),
])
BUILTIN_TEXT_FKJJCW = SpeechsList("builtin_text-FkjJCW").speechs([
    Speech().add_text("""
*Willie* Tu m'as dis de choisir, je choisi hein. Ont pars à l'ouest.
""").set_prob(1),
])
BUILTIN_TEXT_KVYNXR = SpeechsList("builtin_text-KvYNxr").speechs([
    Speech().add_text("""
*Willie* Personnelement, j'ai l'impression que ce serais plus malin de passer par l'ouest, si ont à des soucis sur le chemin, ont pourras revenir plus vite. Toi tu pense qu'il faudrais  plutôt prendre l'est ou l'ouest ?
""").set_prob(1),
])
BUILTIN_TEXT_2_L2CZ = SpeechsList("builtin_text-2-l2cz").speechs([
    Speech().add_text("""
*Willie* Alors, t'en pense quoi ? L'ouest c'est plus rapide mais à été sécurisé il y à moins longtemps, et l'Est est un peu plus long, mais à été sécurisé il y à plus longtemps. Tu pense qu'il faudrais plutôt qu'ont prenne l'Est ou l'Ouest ?
""").set_prob(1),
])
BUILTIN_TEXT_JTO5TM = SpeechsList("builtin_text-Jto5Tm").speechs([
    Speech().add_text("""
*Willie* Pas de soucis si tu n'arrive pas à te décider. Mais ont peut pas y passer la journée, partons à l'ouest. *Léo* Ok, ça me vas.
""").set_prob(1),
])
BUILTIN_TEXT_WITB9K = SpeechsList("builtin_text-witB9K").speechs([
    Speech().add_text("""
*Léo et Willie* *attrape leurs sacs et commencent à marcher*
""").set_prob(1),
])
BUILTIN_TEXT_ZNQCVT = SpeechsList("builtin_text-ZNqCvT").speechs([
    Speech().add_text("""
*Willie* Personnelement j'aurais plutôt pris l'ouest, ça m'as l'air plus intérréssant, car si ont à des soucis sur le chemin, ont pourrais revenir plus vite. Enfin, t'as plus d'expérience que moi sur ce sujet, je te laisse choisir. Ont prend l'Est ou l'Ouest ?
""").set_prob(1),
])
BUILTIN_TEXT_D7WANN = SpeechsList("builtin_text-D7WAnn").speechs([
    Speech().add_text("""
*Willie* Je voulais pas te faire douter hein ! Aller, prenons l'Ouest comme tu disais !
""").set_prob(1),
])
BUILTIN_TEXT_SAMRLY = SpeechsList("builtin_text-SAMrLy").speechs([
    Speech().add_text("""
*Willie* C'est décidé pour l'Est ! Allons-y !
""").set_prob(1),
])
BUILTIN_TEXT_QYTSHY = SpeechsList("builtin_text-qYTShy").speechs([
    Speech().add_text("""
*Willie* C'est décidé pour l'Est ! Allons-y !
""").set_prob(1),
])
BUILTIN_TEXT_IHVBLA = SpeechsList("builtin_text-IHVBla").speechs([
    Speech().add_text("""
*Willie* J'avais en tête la même chose, mais je viens de me demander si les quatres kilomètres de moins vallent le coup qu'il y ai plus de chances de tombé sur des nazis. Bien sûr, il y à très peu de chance, mais ça me fait douter. T'en pense quoi ont prend tout de même l'Ouest ?
""").set_prob(1),
])
BUILTIN_TEXT_BSPKTN = SpeechsList("builtin_text-bsPkTN").speechs([
    Speech().add_text("""
*Willie* T'as raison, je me fait probablement des films. Prenons l'Ouest !
""").set_prob(1),
])
BUILTIN_TEXT_6IRPGA = SpeechsList("builtin_text-6IRpGa").speechs([
    Speech().add_text("""
*Willie* T'as raison, c'est un petit doute à la con, et même si ça se produis pas, quatres kilomètres c'est pas énorme. Partons à l'Est !
""").set_prob(1),
])
BUILTIN_TEXT_E2DI29 = SpeechsList("builtin_text-e2di29").speechs([
    Speech().add_text("""
*Léo* Je pense qu'ont doit pouvoir trouver un meilleur chemin. Après tout ces cartes ont été fait à la vas vite. *Willie* Tu aurais quoi en tête ? Genre escalader la colline ? *Menu* Vous pouvez prendre le temps de calculer avec Willie si escalader une colline est une bonne idée, bien sûr l'idée n'en n'est qu'une parmis d'autres et pourrais ne mener à rien, voulez-vous prendre du temps sur celle-ci ?
""").set_prob(1),
])
BUILTIN_TEXT_IBCGTD = SpeechsList("builtin_text-iBcGTd").speechs([
    Speech().add_text("""
*Léo* Ca pourrait marché, tu peut vérifiez ça ? *Willie* Totalement ! Alors... *sort une règle*, escalader pourrais nous faire gagner 3 kilomètres, donc une demi-heure, il faudrais qu'ont aille chercher de l'équipement pour escalader, au moins 15 minutes, sauf qu'avec l'équipement qui nous allourdis ça nous rallentirais un peu, peut-être de 15 ou 20 minutes. Donc une heure aller retour, c'est vrai, ça nous ferrais gagner un peu de temps ont pourrais faire ça. T'en pense quoi, ont le fait ?
""").set_prob(1),
])
BUILTIN_TEXT_QR7SM_ = SpeechsList("builtin_text-qr7Sm-").speechs([
    Speech().add_text("""
*Willie* Aaaaah, la boulette !
""").set_prob(1),
])
BUILTIN_TEXT_AWUQLV = SpeechsList("builtin_text-AwUqLV").speechs([
    Speech().add_text("""
*Willie* Oui, t'as raison, c'est pas une super idée. Il faudrais qu'ont aille chercher de l'équipement *silence d'une seconde*.
""").set_prob(1),
])
BUILTIN_TEXT_PYERBK = SpeechsList("builtin_text-PyERbk").speechs([
    Speech().add_text("""
*Willie* Je viens de me rendre compte, ont gagne une heure si ont gagne 30 minutes à l'aller et le retour, mais ont pourras pas escalader pour revenir. Donc en faites ça vas pas vraiment nous faire gagner du temps si ont vas chercher l'équipement et qu'ont doit le transporter. Mon idée est pas terrible, en faites. *petit rire* *silence d'une demi seconde *
""").set_prob(1),
])
BUILTIN_TEXT_Q1WB5B = SpeechsList("builtin_text-Q1WB5b").speechs([
    Speech().add_text("""
*Willie* Attend, je réfléchi *silence d'une demi seconde *
""").set_prob(1),
])
BUILTIN_TEXT_8XDBZS = SpeechsList("builtin_text-8xDBzS").speechs([
    Speech().add_text("""
*Willie* Ah ! J'ai une autre idée ! Je sais pas si elle est bien, tu veut tout de même que je te la dise ? 
""").set_prob(1),
])
BUILTIN_TEXT_QUTMSR = SpeechsList("builtin_text-qutMSr").speechs([
    Speech().add_text("""
*Willie* Il y à souvent des véhicules qui partent, ont pourrais appeller la base par radio, pour leur demander si il y à pas une voiture ou un camion qui pars bientôt vers l'Est ou l'Ouest, et lui demander de nous déposer un peu plus tôt que notre destination pour éviter de risquer d'être réperé. T'en pense quoi, tu trouve que c'est une bonne idée ?
""").set_prob(1),
])
BUILTIN_TEXT_5WIVFJ = SpeechsList("builtin_text-5wIVFj").speechs([
    Speech().add_text("""
*Willie* Bon, laisse moi réfléchir, je vais en trouver une autre... *silence d'une demi seconde* Non, je suis officiellement à cours d'idées... Je pense pas qu'ont vas trouver de raccourci, faisons le à pied comme prévu. Regardons la carte une seconde... *silence d'une demi seconde*
""").set_prob(1),
])
BUILTIN_TEXT_EHOMME = SpeechsList("builtin_text-EhOMMe").speechs([
    Speech().add_text("""
*Léo* Demandons ! Tu peut me passer la radio ? *Willie* *attrape la radio de son sac* Tiens. *Léo* *vielle radio qui s'allume* Allo base ? Ici Léo Major avec Willy Arseneault, est-ce que des véhicules s'appretent à partir de la base dans les prochaines minutes vers l'est ou l'ouest ? Terminé. *voix de basse qualité avec effet radio* Bien reçu, un camion de réaprivisionnement vas partir vers l'ouest dans 6 minutes, vous voulez qu'il vienne vous chercher ? Terminé. *bruit radio s'éteins*
""").set_prob(1),
])
BUILTIN_TEXT_EZJCE3 = SpeechsList("builtin_text-eZJcE3").speechs([
    Speech().add_text("""
*Léo* *radio qui s'allume* Bien reçu. Exact, nous sommes juste devant l'entré de la Base, nous seront prêt dès qu'il arrive. Terminé. *radio qui s'éteins* *silence d'une seconde* *voix de base qualité dans la radio* Bien reçu. L'information est transmise, il vas venir vous chercher. Over. *radio qui s'éteins* *Léo* *radio qui s'allume* Over. *radio qui s'éteins*.
""").set_prob(1),
])
BUILTIN_TEXT_LG_D6R = SpeechsList("builtin_text-lG_D6r").speechs([
    Speech().add_text("""
*radio qui s'allume * *Léo* Heeeeu... *Willie* *qui interromps Léo* Bien reçu ! Nous sommes prêt à partir, nous allons attendre le camion. Terminé * radio qui s'éteins * *Willie* Léo, t'aurais du répondre ! *voix de base qualité dans la radio* Bien reçu. L'information est transmise, il vas venir vous chercher. Over. *radio qui s'éteins* *Willie* *radio qui s'allume* Over. *radio qui s'éteins*.
""").set_prob(1),
])
BUILTIN_TEXT_A6A0TS = SpeechsList("builtin_text-a6A0Ts").speechs([
    Speech().add_text("""
*petit bruits d'oiseaux pour signifier que le temps passe* *bruit d'un vieux camion qui arrive avec un vieux moteur, il s'arrête, une grosse porte arrière s'ouvre, bruits de pas sur du métal pour dire que vous monter dedans, la porte se ferme, le camion repars *
""").set_prob(1),
])
BUILTIN_TEXT_1OGURJ = SpeechsList("builtin_text-1OgurJ").speechs([
    Speech().add_text("""
#vous marcher, mais le temps de marche jusqu'à arrivé au même endroit qu'avec le camion est zappé en quelques secondes
""").set_prob(1),
])
BUILTIN_TEXT_R6O0UO = SpeechsList("builtin_text-r6O0Uo").speechs([
    Speech().add_text("""
#vous entendez le camion rouler pendant plusieurs secondes, le bruit s'éteins, silence d'une demi seconde, il se relance, puis il s'arrête, vous dessendez du camion et il repars.
""").set_prob(1),
])
BUILTIN_TEXT_0GDHKW = SpeechsList("builtin_text-0GDHKw").speechs([
    Speech().add_text("""
*Willie* Ont doit avancer vers le nord. *Léo* Ok, gardons l'oeil ouvert, si des gens sont passer par ici, il devrais y avoir des traces.
""").set_prob(1),
])
BUILTIN_TEXT_GUXF_W = SpeechsList("builtin_text-GUxF-W").speechs([
    Speech().add_text("""
*Luc* Alors Willie. T'est toujours un peu bigleu ? Je suppose que tu préfère une arme de courte portée ? *Willie* Si tu a, oui. *Luc* Ok, je pense que j'ai ce qui te faut. *commence à grogner en essayer d'attraper un truc* *Luc* Léo, tu pourrais venir me passer un coup de main ?
""").set_prob(1),
])
BUILTIN_TEXT_HB19NH = SpeechsList("builtin_text-Hb19NH").speechs([
    Speech().add_text("""
*attrape l'arme à deux* *Luc* Merci Léo.
""").set_prob(1),
])
BUILTIN_TEXT_FU541B = SpeechsList("builtin_text-Fu541b").speechs([
    Speech().add_text("""
*Luc* Quoi ? Bon te prend pas la tête, c'est bon je l'ai.
""").set_prob(1),
])
BUILTIN_TEXT_EDJ_HM = SpeechsList("builtin_text-Edj_Hm").speechs([
    Speech().add_text("""
*Luc* Donc, j'ai une Thompson M1921, c'est un pistolet mitrailleur. Tu connais ? *Willie* Oui, tu n'as pas besoin de me donné les détails. *Luc* Alors, t'en pense quoi ?
""").set_prob(1),
])
BUILTIN_TEXT_ZV44QS = SpeechsList("builtin_text-ZV44Qs").speechs([
    Speech().add_text("""
*Willie* J'ai pas l'impression qu'une arme automatique me conviendrais. Je pense que quelque chose au coup par coup, mais à courte porté serait mieux pour moi. *Menu* Souhaitez-vous recommander à Willie de prendre un fusil d'infantrie, un fusil à pompe, ou rester vous silencieux ?
""").set_prob(1),
])
BUILTIN_TEXT_ABA5ZI = SpeechsList("builtin_text-aba5zI").speechs([
    Speech().add_text("""
*Luc* Si tu veut, j'ai une seconde Thompson comme celle que Léo viens de prendre. T'en pense quoi ?
""").set_prob(1),
])
BUILTIN_TEXT_HALUVV = SpeechsList("builtin_text-HALuVV").speechs([
    Speech().add_text("""
*Léo* Willie, tu pourrais prendre un fusil d'infantrie ? *Willie* T'as le temps entre chaque tir ? C'est ça Luc ? *Luc* Oui, par contre, si t'est à très courte proximité, t'as intêret à pas rater. *Willie* C'est pas le cas de toutes les armes ? *Luc* En particulier des fusils d'infantries. Faut vraiment que tu soit sûr. J'ai un vieux fusil à pompe TrenchGun qui traine, cependant qui est toujours aussi efficace et simple à utiliser. Et avec j'ai des munitions standards.
""").set_prob(1),
])
BUILTIN_TEXT_VINC3D = SpeechsList("builtin_text-ViNC3d").speechs([
    Speech().add_text("""
*Luc* Tu pourrais prendre un fusil à pompe Willie. *Willie* T'a raison, de l'image que j'en ai ça m'a l'air bien. *Luc* Ouai, Léo à raison. La portée avec les munitions standard est assez courte, donc tu n'as pas besoin d'être super bon en visé. J'ai un fusil à pompe TrenchGun si tu veut.
""").set_prob(1),
])
BUILTIN_TEXT_RPZFTL = SpeechsList("builtin_text-rpzFtl").speechs([
    Speech().add_text("""
*Willie* J'ai l'air con, mais c'est quoi la portée d'un fusil à pompe avec les munitions standard ? *Luc* Ont parle bien de la portée de la théorique, car la portée réel est vachement influencé par le vent, l'inclinaison du fusil, l'air, l'humidité, la température, la pression atmosphérique, et pleins d'autres paramètres. Mettons au test Léo. Alors Léo, je te laisse 5 secondes pour que tu me dise quelle est la porté théorique d'un fusil à pompe avec les munitions standard. 5 mètres, 20 mètres, 60 mètres ? Combien tu pense ?
""").set_prob(1),
])
BUILTIN_TEXT_PKNDYS = SpeechsList("builtin_text-PkNdyS").speechs([
    Speech().add_text("""
*Luc* Toujours là Léo ? *Léo* Oui, oui, je laisse juste Willie choisir par lui même. *Luc* Ok. L'impression que j'ai, c'est que ce qui te conviendrais bien Willie, c'est un fusil à pompe. Simple à l'emploi, pas besoin d'être un as de la visé quand t'utilise les munitions standard, et très efficace à une assez courte porté. J'ai un fusil à pompe TrenchGun si tu veut. Par contre c'est pas fait pour la moyenne ou grande portée.
""").set_prob(1),
])
BUILTIN_TEXT_JLCPBB = SpeechsList("builtin_text-JlCPbb").speechs([
    Speech().add_text("""
*Luc* Bon c'est pas grave si veut pas jouer. Ca vas juste nous faire perdre du temps de toute façon.
""").set_prob(1),
])
BUILTIN_TEXT_UN_FDG = SpeechsList("builtin_text-UN-fDG").speechs([
    Speech().add_text("""
*Willie* Si tu veut pas choisir Léo, je choisis, commençons par moi. *Léo* Ok, excuse moi je pensais à autre chose.
""").set_prob(1),
])
BUILTIN_TEXT_EYHPU9 = SpeechsList("builtin_text-eYhPU9").speechs([
    Speech().add_text("""
{{state.session.slots.number.value}}
""").set_prob(1),
])
BUILTIN_TEXT_9YEMYC = SpeechsList("builtin_text-9yeMyc").speechs([
    Speech().add_text("""
Donc pour te répondre Willie, plus t'est proche avec un fusil à pompe mieux c'est. C'est parce qu'il ne tire pas qu'une balle, il tire une cartouche qui en quelque sorte explose, et envois des dizaines de balles dans tous les angles différents en face de toi. Tu à un chargeur de 7 cartouches que tu peut tiré assez rapidement. C'est assez similaire à une grenade en faites. C'est pour ça que c'est si simple d'utilisation, mais donc ça commence à sérieusement perdre de l'interêt à partir de 25 mètres. *Willie* Ah, ça m'a l'air bien ! T'en pense quoi Léo, si t'étais moi, tu prendrais le fusil à pompe ?
""").set_prob(1),
])
BUILTIN_TEXT_UGPHCY = SpeechsList("builtin_text-ugpHCY").speechs([
    Speech().add_text("""
*Luc* Tu pense que ça a à ce point de porté ? C'est un peu beaucoup ! *Léo* Je m'y connais pas autant que toi hein ! *petit rire qui s'éteins*
""").set_prob(1),
])
BUILTIN_TEXT_SHC3KR = SpeechsList("builtin_text-ShC3kR").speechs([
    Speech().add_text("""
*Luc* Bien joué, à pas loin prêt c'est ça ! Tu t'y connais plus que ce que j'aurais pensé. *Léo* Hé ben tu crois quoi, j'apprend vite ! *petit rire qui s'éteins*
""").set_prob(1),
])
BUILTIN_TEXT_CWZU_0 = SpeechsList("builtin_text-cWzu-0").speechs([
    Speech().add_text("""
*Willie* Ok ! Bon Luc, je prend le fusil à pompe, TrenchGun c'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_SMB32A = SpeechsList("builtin_text-SMb32A").speechs([
    Speech().add_text("""
*Luc* C'est ça, tiens voilà aussi la sangle du fusil, sa cartouchière est pleinement remplis de 30 cartouches. *passe les armes et les balles* *Menu* Voulez-vous recommander à Wille de prendre une seconde arme ?
""").set_prob(1),
])
BUILTIN_TEXT_UMHHNE = SpeechsList("builtin_text-uMHhne").speechs([
    Speech().add_text("""
*Willie* C'est vrai, moi aussi j'ai quelque doutes Léo... *Luc* Les gars, j'ai vraiment pas mieux. Faut pas que vous tardiez à partir pour votre mission. Prend le fusil à pompe Willie, il t'iras très bien. *Willie* Bon... si tu n'as vraiment pas mieux. C'est un fusil à pompe TrenchGun, c'est ça ?
""").set_prob(1),
])
BUILTIN_TEXT_ADKXX5 = SpeechsList("builtin_text-aDKXx5").speechs([
    Speech().add_text("""
*Léo* Tu devrais également prendre une seconde arme Willie, ça peut être utile. *Willie* Ah, pourquoi pas... C'est possible Luc ? *Luc* Oui pas de soucis. Je suis d'accord avec Léo. Par contre, avec un fusil à pompe un pistolet te seras pas super utile Willie. Attend je vais voir ce que j'ai qui irais bien *cherche un truc* Ahah ! J'ai une machette si tu veut ! *Willie* Pourquoi une machette ? *Luc* Je suis d'accord ça parrais pas très utile, mais ça change tout si tu est en forêt. Et si jamais tu doit l'utiliser pour... autre chose... l'avantage est que tu ne tombe jamais à court de munitions. *Willie* Mhmm... de toute façon c'est pas très encombrant, ça coute rien de la prendre ? *Luc* Non, et de toute façon j'en ai pas mal, donc ça coute rien non plus à qui que ce soit d'autre. *Willie* Ok, je la prend, merci Luc !
""").set_prob(1),
])
BUILTIN_TEXT_SQWO36 = SpeechsList("builtin_text-sQWo36").speechs([
    Speech().add_text("""
*Luc* Tout est bon Willie ? *Willie* Oui, tout est bon !
""").set_prob(1),
])
BUILTIN_TEXT__OMRE2 = SpeechsList("builtin_text--OMRe2").speechs([
    Speech().add_text("""
*Luc* Ont passe à toi Léo ?
""").set_prob(1),
])
BUILTIN_TEXT_QAH3W5 = SpeechsList("builtin_text-qAH3W5").speechs([
    Speech().add_text("""
*il attrape un fusil * Un Lee Enfields marque 4 numéro 1, *pose fusil sur une table *un petit bijou de fusil à levier pour le tire longue distance. La tu déjà utiliser ?
""").set_prob(1),
])
BUILTIN_TEXT_4YPONJ = SpeechsList("builtin_text-4yPoNJ").speechs([
    Speech().add_text("""
*Luc* Alors, pour toi Léo, voyons...*cherche une arme*
""").set_prob(1),
])
BUILTIN_TEXT_7TFTGG = SpeechsList("builtin_text-7tftGG").speechs([
    Speech().add_text("""
*Luc* Parfait, ont est bon pour vous deux !
""").set_prob(1),
])
BUILTIN_TEXT_3OU7EF = SpeechsList("builtin_text-3OU7EF").speechs([
    Speech().add_text("""
Je pense que j'ai ce qui vas vous convenir, on commence par toi Léo ou par Willie ?
""").set_prob(1),
])
BUILTIN_TEXT_SU0F9U = SpeechsList("builtin_text-su0F9u").speechs([
    Speech().add_text("""
Et en terme de pistolets, tu veut que je t'en montre ?
""").set_prob(1),
])
BUILTIN_TEXT_MC6QAF = SpeechsList("builtin_text-mc6QaF").speechs([
    Speech().add_text("""
Je m'en fout de ce que tu pense. T'as pas le choix voila un pistolet TODO: finish this
""").set_prob(1),
])
BUILTIN_TEXT_TJKU_X = SpeechsList("builtin_text-tJku_X").speechs([
    Speech().add_text("""
*Luc* Donc il y à la Thompson que je viens de proposé à Léo. T'a suivi ce que j'avais dis ? *Willie* Oui, tu n'as pas besoin de me répéter les détails. *Luc* Alors, t'en pense quoi ?
""").set_prob(1),
])
BUILTIN_TEXT_ZSIEFU = SpeechsList("builtin_text-ZsIEFU").speechs([
    Speech().add_text("""
*Luc* *pose une arme relativement lourde* J'ai la Thompson M1921 que je viens de montrer a Willie.
""").set_prob(1),
])
BUILTIN_TEXT_OY4ICC = SpeechsList("builtin_text-oY4Icc").speechs([
    Speech().add_text("""
*Luc* Techniquement c'est un pistolet mitrailleur, mais qui est utilisé en tant que fusil d'assult. Tu doit surêment connaitre un minimum, t'as tout de même envie que je te dise les détails ?
""").set_prob(1),
])
BUILTIN_TEXT_PBKMZN = SpeechsList("builtin_text-pbkMzN").speechs([
    Speech().add_text("""
*Luc* Ca m'étonne pas que tu parte sur un classique Léo ! Voici le Webley #todo: ajouter un truc sur les munitions et une bandolière ?
""").set_prob(1),
])
BUILTIN_TEXT_HPSFHW = SpeechsList("builtin_text-hPSFHw").speechs([
    Speech().add_text("""
*Luc* Tu pense que j'ai oublié de te proposer quelque chose ? Attend je réfléchis... *silence d'une demi seconde* Non, non tu à tout. Ah ! Par contre tu à raison, dans tous les cas il faudras pas que vous oublier de signer le registre quand vous aurez fini. *Léo* Ok, très bien !
""").set_prob(1),
])
BUILTIN_TEXT_WNNQHU = SpeechsList("builtin_text-WnNQHu").speechs([
    Speech().add_text("""
*Luc* Ah tu me surprend Léo ! J'aurais cru que tu serais partis sur le classique. Mais t'as raison, il faut bien évoluer avec le temps... Tiens voici le Colt #todo: ajouter un truc sur les munitions et une bandolière ?
""").set_prob(1),
])
BUILTIN_TEXT_O1GYYO = SpeechsList("builtin_text-O1gyyo").speechs([
    Speech().add_text("""
#Purely here to avoid warnings
""").set_prob(1),
])
BUILTIN_TEXT_GZ_JSX = SpeechsList("builtin_text-gz-JSX").speechs([
    Speech().add_text("""
*Luc* Ok, si tu pense que c'est mieux. Je t'avoue que ça me fait peur, mais je te fais confiance.
""").set_prob(1),
])
BUILTIN_TEXT_UYCHLY = SpeechsList("builtin_text-UyCHlY").speechs([
    Speech().add_text("""
*Luc* Ouf, tu m'as fait peur ! Tu veut prendre une arme principale alors ?
""").set_prob(1),
])
BUILTIN_TEXT_2F4_J0 = SpeechsList("builtin_text-2f4_j0").speechs([
    Speech().add_text("""
*Luc* Tu veut prendre le fusil Lee Endfields ou la Thompson ?
""").set_prob(1),
])
BUILTIN_TEXT_1LUB8N = SpeechsList("builtin_text-1luB8n").speechs([
    Speech().add_text("""
*Luc* Tu veut également prendre un pistolet ?
""").set_prob(1),
])
BUILTIN_TEXT_XPRHV9 = SpeechsList("builtin_text-xPRhv9").speechs([
    Speech().add_text("""
*Luc* Tu vas prendre un pistolet tout de même ?
""").set_prob(1),
])
BUILTIN_TEXT_F7D2DK = SpeechsList("builtin_text-F7d2Dk").speechs([
    Speech().add_text("""
*Luc* *un peu ennuyé et désespéré* Bon, c'est pas grave si tu veut pas prendre d'arme principal, je te fais confiance...
""").set_prob(1),
])
BUILTIN_TEXT_R2FQ5E = SpeechsList("builtin_text-r2FQ5e").speechs([
    Speech().add_text("""
*Luc* Léo ? Sérieusement ? J'avais que tu me fait peur, mais je te fait confiance. Je vais pas te forcer à prendre une arme. *silence d'une demi seconde*
""").set_prob(1),
])
BUILTIN_TEXT_VJBSMQ = SpeechsList("builtin_text-VJbsmq").speechs([
    Speech().add_text("""
Des pistolets que je peut te donner, tu veut prendre le premier le Colt, ou le second le Webley ?
""").set_prob(1),
])
BUILTIN_TEXT_D_LQO9 = SpeechsList("builtin_text-d_LQo9").speechs([
    Speech().add_text("""
*Léo* Oui, t'inquiète pas Luc. *Luc* Très bien, si tu est certain. Ont passe à Willie alors ?
""").set_prob(1),
])
BUILTIN_TEXT__UJGHQ = SpeechsList("builtin_text-_uJgHq").speechs([
    Speech().add_text("""
#todo: fix the section below, because right now, it will send to the conflict between luc and willie, even if willie has not already taken his weapons
""").set_prob(1),
])
