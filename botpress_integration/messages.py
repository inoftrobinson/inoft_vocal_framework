from inoft_vocal_framework.speechs.ssml_builder_core import Speech, SpeechsList


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
* Ambience...* *Enorme alarme et une personne gueulant dans une radio* C'est pas le jour pour dormir ! Réveiller-vous, j'attend tout le monde sur le au centre du camp dans 3 minutes !
* Tu te lève et tu commence à t'habiller * Hey Léo, bien dormi ?
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
Pareil, j'ai à peine dormi. T'était pareil lors de ta première fois ?
""").set_prob(1),
    
])

BUILTIN_TEXT__FWW96 = SpeechsList("builtin_text--FWw96").speechs([
    
    Speech().add_text("""
T'a de la chance. J'ai à peine dormi, t'était pareil avant ta première fois ?
""").set_prob(1),
    
])

BUILTIN_TEXT_WQHTNB = SpeechsList("builtin_text-wqhtNB").speechs([
    
    Speech().add_text("""
Ouai....* sigh* Bon de toute façon, c'est pour le bien, hein. La ont plus vraiment le choix de toute façon * laughing * C'est bon t'est prêt ?
""").set_prob(1),
    
])

BUILTIN_TEXT_VOCLDO = SpeechsList("builtin_text-VOcldO").speechs([
    
    Speech().add_text("""
Quoi ? Je suis vraiment mal réveillé. J'ai pas réussi à dormir, c'était pareil ta première fois ?
""").set_prob(1),
    
])

BUILTIN_TEXT_GZ5LMT = SpeechsList("builtin_text-GZ5Lmt").speechs([
    
    Speech().add_text("""
On vraiment pas le temps Léo, aller viens. ** walking ** Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
    
])

BUILTIN_TEXT_NIVD2C = SpeechsList("builtin_text-NiVD2C").speechs([
    
    Speech().add_text("""
Ok super, allons-y. ** walking ** Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
    
])

BUILTIN_TEXT_CLAWQ0 = SpeechsList("builtin_text-Clawq0").speechs([
    
    Speech().add_text("""
De toute façon, faut qu'y aille. ** walking ** Tout le monde est là ? ** à plusieurs ** Oui Chef ! ** en criant ** J'ai rien entendu !
""").set_prob(1),
    
])

BUILTIN_TEXT_LHJGU5 = SpeechsList("builtin_text-LHJgU5").speechs([
    
    Speech().add_text("""
T'essais de faire le malin Leo ?
""").set_prob(1),
    
])

BUILTIN_TEXT_0MCHOO = SpeechsList("builtin_text-0McHoo").speechs([
    
    Speech().add_text("""
Tu te fous de moi ?
""").set_prob(1),
    
])

BUILTIN_TEXT_AMLZRX = SpeechsList("builtin_text-aMlZRX").speechs([
    
    Speech().add_text("""
C'est bien ce que je croyait. ** ton pote ** Léo, arrête de déconner ! Ok ?
""").set_prob(1),
    
])

BUILTIN_TEXT_GQUBNB = SpeechsList("builtin_text-gQuBnb").speechs([
    
    Speech().add_text("""
** gant te fouette * C'est pas le jour pour déconner, reprend toi en main ! ** (le pote) ** Léo, arrête de déconner ! Ok ?
""").set_prob(1),
    
])

BUILTIN_TEXT_DJKP2N = SpeechsList("builtin_text-dJKP2N").speechs([
    
    Speech().add_text("""
Vous jouerez Léo Major, éclaireur des forces canadiennes agé de toute juste 23 ans. Votre histoire commençeras durant la bataille de l'Escaut, qui c'est produite du 2 octobre jusqu'au 8 novembre 1944. 135 000 soldats canadien, français britannique, polandais, américain, belges, néérlendais, et norvègien sont opposé a 90 000 soldats allemands. Cette opération à comme objectif d'ouvrir une route de ravitaillement vers la ville belge d'Anvers, pour pouvoir ravitailler en armes, hommes et ressources les forces alliés dans tout le reste du nord-ouest de l'Europe. Cette histoire raconte des faits réels, les choix auxquelles vont serez confrontés, ont réelement vécu été vécu par Léo Major en 1944. Etes-vous prêt à jouer ?
""").set_prob(1),
    
])

BUILTIN_TEXT_MVDSF5 = SpeechsList("builtin_text-mvdSF5").speechs([
    
    Speech().add_text("""
* général * Cela fait 8 jours que nous avançons. Certains d'entre vous ne le savent pas, mais depuis hier ces salauds de nazis innonde tous les endroits pratiquables autour de la rivière d'Anvers. Seulement nos véhicules amphibiques peuvent avancer, cependant plus de 230 hommes ont déjà été perdu à essayer ça. Nous avons besoin d'éclaireurs agile pour identifier les véhicules qu'ils utilisent pour transporter l'eau. Nous avons besoin de 2 personnes. Des volontaires ?
""").set_prob(1),
    
])

BUILTIN_TEXT_9JHDUX = SpeechsList("builtin_text-9jHdux").speechs([
    
    Speech().add_text("""
** ton pote ** Léo et moi sommes prêt ! Pas vrai Léo ?
""").set_prob(1),
    
])

BUILTIN_TEXT_PODCGV = SpeechsList("builtin_text-podcGV").speechs([
    
    Speech().add_text("""
Très bien Léo ! Je suppose que ** nom de pote ** t'accompegneras ? * ton pote * Oui chef ! Très bien, c'est décidé, vous partirez dans 30 minutes.
""").set_prob(1),
    
])

BUILTIN_TEXT_H7OF88 = SpeechsList("builtin_text-H7Of88").speechs([
    
    Speech().add_text("""
* chef * Très bien, c'est décidé. Vous partirez dans 30 minutes.
""").set_prob(1),
    
])