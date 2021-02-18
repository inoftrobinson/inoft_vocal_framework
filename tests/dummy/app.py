import os
from inoft_vocal_framework import InoftSkill, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback


class StartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self) -> dict:
        self.say("Moi j'adorerais le nouveau format")
        self.google.request_push_notifications_permission_if_missing()
        self.memorize_session_then_state(NumPlayersStateHandler)
        # self.unity.call_function("character.jump();"
        #                         "truck.destroy();")
        return self.to_platform_dict()

class GoLeft(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_in_intent_names("GoLeft") and self.persistent_remember("level").to_int(default=None) > 10

    def handle(self) -> dict:
        current_level = self.persistent_remember("current_level").to_int(default=None)
        if current_level is None:
            raise Exception(f"Dude the level")

        new_speed = 0.5 * current_level
        self.unity.call_function(f"from bidulechouette import character"
                                 f"character.go_left(speed={new_speed});")
        return self.to_platform_dict()


class Caca(InoftStateHandler):
    def handle(self) -> dict:
        pass

class NumPlayersStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.is_in_intent_names("NumberIntent"):
            player_number_value = self.get_intent_arg_value("number")
            if player_number_value is not None:
                self.persistent_memorize("lastGameUnconfirmedPlayerNumbers", player_number_value)
                self.say(f"{player_number_value} joueurs, c'est ça ?")
                self.memorize_session_then_state(ConfirmNumPlayersStateHandler)
                return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("Combien de joueurs ?")
        return self.to_platform_dict()


class ConfirmNumPlayersStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.is_in_intent_names("AMAZON.YesIntent"):
            num_players = self.persistent_remember("lastGameUnconfirmedPlayerNumbers", int)
            if num_players is not None:
                players_list = list()
                for i_player in range(num_players):
                    players_list.append(dict())

                self.persistent_memorize("lastGamePlayersList", players_list)
                self.persistent_forget("lastGameUnconfirmedPlayerNumbers")
                self.memorize_session_then_state(DefinePlayerNamesStateHandler)

                DefinePlayerNamesStateHandler(self).ask_player_name_if_needed()
                return self.to_platform_dict()

            self.say("J'ai oublié, combien de joueur vouliez-vous ?")
            self.memorize_session_then_state(NumPlayersStateHandler)
            return self.to_platform_dict()

        elif self.is_in_intent_names("AMAZON.NoIntent"):
            self.say("Pourquoi ?")
            return self.to_platform_dict()

    def fallback(self) -> dict:
        return self.handle()


class DefinePlayerNamesStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.is_in_intent_names("PlayerName"):
            played_list_id = self.persistent_remember("lastPlayerListIdToSetName", int)
            if played_list_id is not None:
                players_list = self.persistent_remember("lastGamePlayersList", list)
                players_list[played_list_id]["name"] = self.get_intent_arg_value("name")
                self.persistent_memorize("lastGamePlayersList", players_list)

        if self.ask_player_name_if_needed() is True:
            return self.to_platform_dict()
        else:
            return DecisionStateHandler(self).handle()

    def ask_player_name_if_needed(self):
        players_list = self.persistent_remember("lastGamePlayersList", list)
        if players_list is not None:
            for i_player, player_dict in enumerate(players_list):
                if "name" not in player_dict.keys():
                    self.say(f"Joueur {i_player + 1} quelle est votre prénom ?")
                    self.memorize_session_then_state(DefinePlayerNamesStateHandler)
                    self.persistent_memorize("lastPlayerListIdToSetName", i_player)
                    return True

    def fallback(self) -> dict:
        return self.handle()


class DecisionStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        players_list = self.persistent_remember("lastGamePlayersList", list)
        indexes_players_that_participated = self.persistent_remember("IndexesPlayersThatParticipatedInCurrentDecisionRound", list)

        if indexes_players_that_participated is not None:
            cleaned_players_list = list()
            for i_player, player_dict in enumerate(players_list):
                if i_player not in indexes_players_that_participated:
                    cleaned_players_list.append(player_dict)
            players_list = cleaned_players_list

        if players_list is not None:
            from random import sample as random_sample
            for i_player, player_dict in enumerate(random_sample(players_list, len(players_list))):
                player_name = player_dict["name"] if "name" in player_dict.keys() else i_player
                self.say(f"{player_name} quelle est votre décision ?")
                self.memorize_session_then_state(DecisionStateHandler)
                indexes_players_that_participated.append(i_player)
                self.persistent_memorize("IndexesPlayersThatParticipatedInCurrentDecisionRound", indexes_players_that_participated)
                # todo: fix that and memorize not when asking to take the decision, but when taking it
                return self.to_platform_dict()

        self.say("Super, toutes les décisions ont été prises.")
        return self.to_platform_dict()




class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        return StartRequestHandler(self).handle()
        self.say("I have no idea what you want to say")
        return self.to_platform_dict()


def lambda_handler(event, context):
    from app_settings import settings
    skill_builder = InoftSkill(settings_instance=settings)
    skill_builder.add_request_handler(StartRequestHandler)
    skill_builder.add_state_handler(NumPlayersStateHandler)
    skill_builder.add_state_handler(ConfirmNumPlayersStateHandler)
    skill_builder.add_state_handler(DefinePlayerNamesStateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)


if __name__ == "__main__":
    from inoft_vocal_framework import Simulator
    """from inoft_vocal_engine import start_discord_listening
    from inoft_vocal_engine.platforms_handlers.discord.static_token import token
    start_discord_listening(token=token, lambda_handler_function=lambda_handler)"""
    event_, context_ = Simulator(platform=Simulator.PLATFORM_ALEXA, event_type="launch").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
