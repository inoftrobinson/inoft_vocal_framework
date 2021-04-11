from inoft_vocal_framework import InoftRequestHandler, AudioBlock, InoftStateHandler, InoftSkill, Settings, \
    InoftDefaultFallback


class StartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track2 = audio_block.create_track(primary=True)
        track2_speech1 = track2.create_speech(
            text="Willie viens de poser l'opérateur radio endormis par terre. Ils sont teux deux à environ cinquainte centimètres de vous. A peine suffisamment près pour légèrement distingué les cheveux marrons de Willie, et les cheveux blond de l'opérateur radio, et rien d'autre.",
            voice_key="Mathieu", player_start_time=track2.player_start_time
        )
        track2_speech3 = track2.create_speech(
            text="Si ont veut qu'il nous soit utile, il faut pas qu'il pose de soucis quand il vas se réveillé. Il faudrais qu'on l'attache.",
            voice_key="Lea", player_start_time=track2_speech1.player_end_time
        )
        track2_speech5 = track2.create_speech(
            text="L'opérateur radio est légèrement en train de bouger sa tête de droite à gauche. Il a toujours les yeux fermés.",
            voice_key="Mathieu", player_start_time=track2_speech3.player_end_time
        )
        self.play_audio_block(audio_block)
        self.memorize_session_then_state(f4fbStateHandler)
        return self.to_platform_dict()

        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track1_speech1 = track1.create_speech(
            text="Willie à l'air particulièrement tendu. Vous pourriez faire ce qu'il vous demande et trouver de quoi attacher l'opérateur radio, ou alors demander à Willie que ce soit vous qui restiez avec l'opérateur radio. Qu'allez-vous faire, chercher ce qu'il faut ou restez avec l'opérateur ?",
            voice_key="Mathieu", player_start_time=track1.player_start_time
        )
        self.play_audio_block(audio_block)
        self.memorize_session_then_state(f4fbStateHandler)
        return self.to_platform_dict()
        track2_speech2 = track2.create_speech(
            text="Willie viens de frapper l'opérateur radio dans le visage. Il ne bouge plus sa tête de droite à gauche.",
            voice_key="Mathieu", player_start_time=track2_speech5.player_end_time
        )
        track2_speech4 = track2.create_speech(
            text="Je reste avec l'opérateur radio au cas où il se réveille. Trouve quelque chose pour l'attacher aussi vite que possible, il faut que l'un de nous monte la garde à l'entrée de la tente.",
            voice_key="Lea", player_start_time=track2_speech2.player_end_time
        )


class f4fbStateHandler(InoftStateHandler):
    def handle(self):
        if self.is_in_intent_names('stay'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech2 = track1.create_speech(
                text="Vas-y toi. Je préfère rester avec l'opérateur radio.",
                voice_key="Lea", player_start_time=track1.player_start_time
            )
            track1_speech3 = track1.create_speech(
                text="Je sais mieux géré ce type de situations ! Fait moi confiance ! Je reste avec l'opérateur radio et tu vas chercher ce qu'il faut pour l'attacher !",
                voice_key="Lea", player_start_time=track1_speech2.player_end_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="La tente de communication est étonnamment très bien isolé du soleil sans son entrée ouverte. Vous ne voyez à peine ce qu'il y à devant vous. Vous réussi à apercevoir la forme d'une lampe éteinte en face de vous à environ 50 centimètres de l'entrée de la tente. C'est probablement la lampe que l'opérateur radio à éteins avant de sortir.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous pourriez allumer la lampe avec le briquet que vous avez sur vous pour avoir une grande visibilité. Ou alors vous éclairé entièrement avec votre briquet, ce qui vous donneras une moins grande visibiblité et est plus discret. Avec quoi allez-vous vous éclairer, la lampe ou votre briquet ?",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            self.memorize_session_then_state(d963StateHandler)
            return self.to_platform_dict()
            track1_speech1 = track1.create_speech(
                text="Hhm...", voice_key="Lea", player_start_time=track1_speech3.player_end_time
            )
        if self.is_in_intent_names('leave'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Ok, garde le en joue, je reviens.", voice_key="Lea",
                player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)


class d963StateHandler(InoftStateHandler):
    def handle(self):
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech2 = track1.create_speech(
                text="Vous vous diriger vers la lampe et passer juste à coté de Willie. Vous apercevez la forme du canon de son fusil à pompe pointé vers l'opérateur radio. Dans l'obscurité Willie n'a même pas remarquer que vous passiez à coté de lui.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous pouvez regarder chacun des objets sur la table un par un. Auquel voulez-vous prêter attention. Le livre, les fils électriques, la tasse ou la corde ?",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            self.memorize_session_then_state(_2d98StateHandler)
            return self.to_platform_dict()
            track1_speech1 = track1.create_speech(
                text="Vous prenez la lampe en main, c'est une lampe au pétrole avec un \"engrenage\" sur son coté pour baisser ou monter le débit de pétrole.",
                voice_key="Mathieu", player_start_time=track1_speech2.player_end_time
            )
            track1_speech3 = track1.create_speech(
                text="La lampe s'allume, vous apercevez bien plus clairement vos alentours. Willie est à 5 mètres de vous, et grâce à la lumière, vous remarquer la tension présente dans son visage.",
                voice_key="Mathieu", player_start_time=track1_speech1.player_end_time
            )
            track1_speech4 = track1.create_speech(
                text="Vous voyez une table juste en face de vous.",
                voice_key="Mathieu", player_start_time=track1_speech3.player_end_time
            )
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech3 = track1.create_speech(
                text="Votre briquet s'allume. La lumière qu'il dégage vous permet de voir relativement bien jusqu'à un mètre. Suffisamment pour voir ce qu'il y à devant vous, mais pas suffisamment pour voir Willie ou pour ne pas vous déplacer avec précautions.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            track1_speech2 = track1.create_speech(
                text="Léo, ça avance ? Grouille toi, il faut qu'on monte la garde !",
                voice_key="Lea", player_start_time=track1_speech3.player_end_time
            )
            track1_speech1 = track1.create_speech(
                text="Presqu *interrompu*", voice_key="Lea", player_start_time=track1_speech2.player_end_time
            )
            track1_speech4 = track1.create_speech(
                text="Vous venez de vous cogner las jambes dans une table en bois.",
                voice_key="Mathieu", player_start_time=track1_speech1.player_end_time
            )


class _2d98StateHandler(InoftStateHandler):
    def handle(self):
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous prenez le livre en main. Il est plus lours que ce qu'il en à l'air. Il doit peser au moins 2 kilos.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            track1_speech2 = track1.create_speech(
                text="Hhm...", voice_key="Lea", player_start_time=track1_speech1.player_end_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous avez déjà lu et pris la dernière page du le livre. Le livre n'as plus aucune utilité.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous venez de reposer le livre sur la table.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous prenez la tasse dans votre main droite. Vous voyez des traces de lèvres sur le coté de la tasse. Quelqu'un à récemment bu dedans.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous regardez l'intérieur de la tasse, elle est totalement vide.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous repossez la tasse sur la table.", voice_key="Mathieu",
                player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Les cables de barbelés sont légèrement rouillé. Vous n'aviez jamais vu de près des cables allemands. Le coeur du cable est un long cable gris foncé métallique d'environ 10 centimètres de largeur et d'épaisseur. Puis tout autour du cable principale, il y à de tous coté des pointes tranchantes faites à partir du même métériaux que le cable principale. Chacun peut-être d'une vingtaine centimètres de long, et à une interval d'environ une pointe tous les 15 centimètres. Il est très mal enroulé, vous avez du mal à juger la longueur du cable, mais il à l'air d'être long de 3 ou 4 mètres.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous pourriez ramener le cable de barbelé à WIllie pour que vous poussiez attacher l'opérateur radio. Vous n'êtes pas obliger de prendre le cable de barbelé maintenant. Si vous le prenez le maintenant, vos mains seront pleines et vous ne pourrez pas regarder ou prendre d'autres objets sur la table. Qu'allez-vous faire, prendre le cable maintenant, ou regarder les autres objets ?",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            self.memorize_session_then_state(bf5aStateHandler)
            return self.to_platform_dict()
        if self.is_in_intent_names('Intention non trouvée'):
            pass


class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("I did not catch that.")
        return self.to_platform_dict()


class bf5aStateHandler(InoftStateHandler):
    def handle(self):
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech4 = track1.create_speech(
                text="Vous prenez le cable en main.", voice_key="Mathieu",
                player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech1 = track1.create_speech(
                text="Vous pourriez vous mettre les gants sur les mains pour moins risquer de vous blesser en portant le cable. Ou alors, vous pourriez aussi le porter à mains nu. Qu'allez-vous faire, mettre les gant ou porter le cable a mains nu ?",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            self.memorize_session_then_state(_77aaStateHandler)
            return self.to_platform_dict()
        if self.is_in_intent_names('Intention non trouvée'):
            pass


class _77aaStateHandler(InoftStateHandler):
    def handle(self):
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech2 = track1.create_speech(
                text="Vous enfilez les gants avec un peu de difficulté, ils sont trop petits pour vos mains.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
        if self.is_in_intent_names('Intention non trouvée'):
            audio_block = AudioBlock()
            track1 = audio_block.create_track(primary=True)
            track1_speech3 = track1.create_speech(
                text="Vous attrapez le cable en essayant de le prendre entre les pointes.",
                voice_key="Mathieu", player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)


def lambda_handler(event, context):
    skill_builder = InoftSkill(Settings())
    skill_builder.add_request_handler(StartRequestHandler)
    skill_builder.add_state_handler(f4fbStateHandler)
    skill_builder.add_state_handler(d963StateHandler)
    skill_builder.add_state_handler(_2d98StateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)


if __name__ == "__main__":
    from inoft_vocal_framework import Simulator

    event1_, context1_ = Simulator(platform=Simulator.PLATFORM_ALEXA, event_type="launch").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event1_, context=context1_)}")

    event2_, context2_ = Simulator(platform=Simulator.PLATFORM_ALEXA, event_type="say_i_stay").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event2_, context=context2_)}")
