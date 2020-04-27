from inoft_vocal_framework import InoftSkill, InoftCondition, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback
from messages import *
import os

class YesCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Yes"])

class TwopersonsCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Twopersons"])

class WithmeCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Withme"])

class WithwillieCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Withwillie"])

class RifleCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Rifle"])

class ThompsonCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Thompson"])

class ColtCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Colt"])

class WebleyCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Webley"])

class FirstCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["First"])

class SecondCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Second"])

class WithlucCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Withluc"])

class AmmoCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Ammo"])

class FirstaidkitCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Firstaidkit"])

class ShotgunCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Shotgun"])

class NumberCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["Number"])

class EntryRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_ZDOKTC.pick())
        self.memorize_session_then_state(EntryStateHandler)
        return self.to_platform_dict()

class EntryStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HH2NQ5.pick())
            self.memorize_session_then_state(NodeFddTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_XSNW_U.pick())
            self.memorize_session_then_state(NodeCdbSevenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFddTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_B7RMGS.pick())
            self.memorize_session_then_state(NodeAThirtyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_VH1ZDV.pick())
            self.memorize_session_then_state(NodeNineThousandAndSeventyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeCdbSevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_B7RMGS.pick())
            self.memorize_session_then_state(NodeAThirtyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_VH1ZDV.pick())
            self.memorize_session_then_state(NodeNineThousandAndSeventyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNineThousandAndSeventyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_9XLAKD.pick())
            self.memorize_session_then_state(NodeZeroSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_M85FOA.pick())
            self.memorize_session_then_state(NodeFortyOneaStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAThirtyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4H2MTU.pick())
            self.memorize_session_then_state(NodeOneaEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9X2NQK.pick())
            self.memorize_session_then_state(NodeFFortyEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeZeroSixtyEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_CMIXBA.pick())
            self.memorize_session_then_state(NodeTwentyThreeSevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_P6DAJE.pick())
            self.memorize_session_then_state(NodeFortyEightaStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFortyOneaStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_YWSRMC.pick())
            self.memorize_session_then_state(NodeSevenEightySevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GEEC4H.pick())
            self.memorize_session_then_state(NodeNineThousandEightHundredAndThirtyFourStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwentyThreeSevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if TwopersonsCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4H2MTU.pick())
            self.memorize_session_then_state(NodeOneaEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9X2NQK.pick())
            self.memorize_session_then_state(NodeFFortyEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFortyEightaStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if TwopersonsCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4H2MTU.pick())
            self.memorize_session_then_state(NodeOneaEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9X2NQK.pick())
            self.memorize_session_then_state(NodeFFortyEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNineThousandEightHundredAndThirtyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if TwopersonsCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4H2MTU.pick())
            self.memorize_session_then_state(NodeOneaEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9X2NQK.pick())
            self.memorize_session_then_state(NodeFFortyEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenEightySevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if TwopersonsCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4H2MTU.pick())
            self.memorize_session_then_state(NodeOneaEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9X2NQK.pick())
            self.memorize_session_then_state(NodeFFortyEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFFortyEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_3OU7EF.pick())
            self.memorize_session_then_state(NodeENinetyOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_2I2WB4.pick())
            self.memorize_session_then_state(NodeFourHundredAndEightySixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneaEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_3OU7EF.pick())
            self.memorize_session_then_state(NodeENinetyOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UFHEEC.pick())
            self.say(BUILTIN_TEXT_3OU7EF.pick())
            self.memorize_session_then_state(NodeFourHundredAndTwentyStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFourHundredAndEightySixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_3OU7EF.pick())
            self.memorize_session_then_state(NodeENinetyOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UFHEEC.pick())
            self.say(BUILTIN_TEXT_3OU7EF.pick())
            self.memorize_session_then_state(NodeFourHundredAndTwentyStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeENinetyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithmeCondition(self).can_handle():
            self.persistent_memorize("leoHasChosenWeaponsFirst", True)
            self.say(BUILTIN_TEXT_WWR0VE.pick())
            self.say(BUILTIN_TEXT_QAH3W5.pick())
            self.memorize_session_then_state(NodeSixaThreeStateHandler)
            return self.to_platform_dict()

        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_8RRKTF.pick())
            self.memorize_session_then_state(NodeOneThousandFiveHundredAndSeventySixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAaThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_O1GYYO.pick())
            self.memorize_session_then_state(NodeNinetyFourSixStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_LI_7KX.pick())
            self.memorize_session_then_state(NodeEdFortyNineStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEdFortyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_RNZGHM.pick())
            self.memorize_session_then_state(NodeSevenHundredAndThirtyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_O1GYYO.pick())
            self.memorize_session_then_state(NodeNinetyFourSixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenHundredAndThirtyThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_O1GYYO.pick())
            self.memorize_session_then_state(NodeNinetyFourSixStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_O1GYYO.pick())
            self.memorize_session_then_state(NodeNinetyFourSixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixHundredAndFiftyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_ZHTAW1.pick())
            self.memorize_session_then_state(NodeSixHundredAndTwentyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_IFLIAH.pick())
            self.memorize_session_then_state(NodeSixtyNineEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixHundredAndTwentyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_LX33H9.pick())
        self.memorize_session_then_state(NodeSixTwentyStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixTwentyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.say(BUILTIN_TEXT_RWXHVL.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeOneHundredAndFortySevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_NVNHUV.pick())
            self.memorize_session_then_state(NodeThirtyNineEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixtyNineEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_LX33H9.pick())
        self.memorize_session_then_state(NodeSixTwentyStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFZeroZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_P2E4QQ.pick())
            self.memorize_session_then_state(NodeSevenSevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_YLIZXR.pick())
            self.memorize_session_then_state(NodeSevenThousandSixHundredAndSixtyNineStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThirtyNineEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_PWRVAK.pick())
            self.say(BUILTIN_TEXT_KWM6JG.pick())
            self.memorize_session_then_state(NodeEightThousandFiveHundredAndSeventyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GJL_UL.pick())
            self.memorize_session_then_state(NodeNinetyThreefStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightThousandFiveHundredAndSeventyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VW2TQR.pick())
            self.memorize_session_then_state(NodeTwoThousandThreeHundredAndThirtyTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_VW2TQR.pick())
            self.memorize_session_then_state(NodeTwoThousandThreeHundredAndThirtyTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNinetyThreefStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_PWRVAK.pick())
            self.say(BUILTIN_TEXT_KWM6JG.pick())
            self.memorize_session_then_state(NodeEightThousandFiveHundredAndSeventyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_BFZB1M.pick())
            self.memorize_session_then_state(NodeAdFiveStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAdFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_BFZB1M.pick())
            self.say(BUILTIN_TEXT_D_LQO9.pick())
            self.memorize_session_then_state(NodeDbfZeroStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_R2FQ5E.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeSixtySevenEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveThirtyEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_NGYXJZ.pick())
            self.memorize_session_then_state(NodeFiveThousandFourHundredAndSixteenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_VW2TQR.pick())
            self.memorize_session_then_state(NodeTwoThousandThreeHundredAndThirtyTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenSevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.say(BUILTIN_TEXT_RWXHVL.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeOneHundredAndFortySevenStateHandler)
            return self.to_platform_dict()

        if ThompsonCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenThompson", True)
            self.say(BUILTIN_TEXT_KJWU5Q.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeThreeOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_BP53AC.pick())
            self.memorize_session_then_state(NodeTwoTwentyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenThousandSixHundredAndSixtyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.say(BUILTIN_TEXT_RWXHVL.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeOneHundredAndFortySevenStateHandler)
            return self.to_platform_dict()

        if ThompsonCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenThompson", True)
            self.say(BUILTIN_TEXT_KJWU5Q.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeThreeOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_BP53AC.pick())
            self.memorize_session_then_state(NodeTwoTwentyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoTwentyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.say(BUILTIN_TEXT_RWXHVL.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeOneHundredAndFortySevenStateHandler)
            return self.to_platform_dict()

        if ThompsonCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenThompson", True)
            self.say(BUILTIN_TEXT_KJWU5Q.pick())
            self.say(BUILTIN_TEXT_SU0F9U.pick())
            self.memorize_session_then_state(NodeThreeOneStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_9E8F4U.pick())
            self.memorize_session_then_state(NodeOneHundredAndThirtyThreeStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_KWM6JG.pick())
            self.memorize_session_then_state(NodeFiveThirtyEightStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneHundredAndFortySevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_KWM6JG.pick())
            self.memorize_session_then_state(NodeFiveThirtyEightStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneHundredAndThirtyThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_PWRVAK.pick())
            self.say(BUILTIN_TEXT_KWM6JG.pick())
            self.memorize_session_then_state(NodeEightThousandFiveHundredAndSeventyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GJL_UL.pick())
            self.memorize_session_then_state(NodeNinetyThreefStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveThousandFourHundredAndSixteenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_K2XS_X.pick())
            self.memorize_session_then_state(NodeSixtyEightbStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_RSNBPG.pick())
            self.memorize_session_then_state(NodeFiveHundredAndThirtyFiveStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoThousandThreeHundredAndThirtyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_K2XS_X.pick())
            self.memorize_session_then_state(NodeSixtyEightbStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_RSNBPG.pick())
            self.memorize_session_then_state(NodeFiveHundredAndThirtyFiveStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixtyEightbStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if ColtCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenColt", True)
            self.memorize_session_then_state(NodeFThreeHundredAndSeventyTwoStateHandler)
            return self.to_platform_dict()

        if WebleyCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenWebley", True)
            self.memorize_session_then_state(NodeOnebTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_A7TOU4.pick())
            self.memorize_session_then_state(NodeThreeThousandThreeHundredStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveHundredAndThirtyFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT__QPGCU.pick())
        self.memorize_session_then_state(NodeAFiveHundredAndThirtyFiveStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeThousandThreeHundredStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if ColtCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenColt", True)
            self.memorize_session_then_state(NodeFThreeHundredAndSeventyTwoStateHandler)
            return self.to_platform_dict()

        if FirstCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenColt", True)
            self.memorize_session_then_state(NodeFThreeHundredAndSeventyTwoStateHandler)
            return self.to_platform_dict()

        if WebleyCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenWebley", True)
            self.memorize_session_then_state(NodeOnebTwoStateHandler)
            return self.to_platform_dict()

        if SecondCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenWebley", True)
            self.memorize_session_then_state(NodeOnebTwoStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFThreeHundredAndSeventyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_WNNQHU.pick())
            self.say(BUILTIN_TEXT_4JO_6P.pick())
            self.memorize_session_then_state(NodeSixteenSixStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_WNNQHU.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeBSixHundredAndSeventyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOnebTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_PBKMZN.pick())
            self.say(BUILTIN_TEXT_4JO_6P.pick())
            self.memorize_session_then_state(NodeSixteenSixcopyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PBKMZN.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeBSixHundredAndSeventyOnecopyStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAFiveHundredAndThirtyFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_A7TOU4.pick())
        self.memorize_session_then_state(NodeThreeThousandThreeHundredStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBcThirtyFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_I3GXVQ.pick())
        self.memorize_session_then_state(NodeSeventyThreeEightStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneSixtySixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSeventyThreeEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GZ_JSX.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeFiveSevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UYCHLY.pick())
            self.memorize_session_then_state(NodeEightyEightThreeStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixaThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_MIBBFS.pick())
            self.memorize_session_then_state(NodeSixHundredAndFiftyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_ZHTAW1.pick())
            self.memorize_session_then_state(NodeSixHundredAndTwentyFourStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneThousandFiveHundredAndSeventySixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithmeCondition(self).can_handle():
            self.persistent_memorize("leoHasChosenWeaponsFirst", True)
            self.say(BUILTIN_TEXT_WWR0VE.pick())
            self.say(BUILTIN_TEXT_QAH3W5.pick())
            self.memorize_session_then_state(NodeSixaThreeStateHandler)
            return self.to_platform_dict()

        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UN_FDG.pick())
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeTwoZeroStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenHundredAndFiftyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFourHundredAndTwentyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithmeCondition(self).can_handle():
            self.persistent_memorize("leoHasChosenWeaponsFirst", True)
            self.say(BUILTIN_TEXT_WWR0VE.pick())
            self.say(BUILTIN_TEXT_QAH3W5.pick())
            self.memorize_session_then_state(NodeSixaThreeStateHandler)
            return self.to_platform_dict()

        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_8RRKTF.pick())
            self.memorize_session_then_state(NodeOneThousandFiveHundredAndSeventySixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBNineHundredAndNinetyFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_MVUC4A.pick())
            self.say(BUILTIN_TEXT_4JO_6P.pick())
            self.memorize_session_then_state(NodeOneThousandSevenHundredAndThirteenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_MVUC4A.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeOneSixtySixStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOneThousandSevenHundredAndThirteenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_HPSFHW.pick())
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeThreeTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoHundredAndEightyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT__QGWUF.pick())
            self.say(BUILTIN_TEXT_4JO_6P.pick())
            self.memorize_session_then_state(NodeEightHundredAndNinetyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT__QGWUF.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeBfFortyTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightHundredAndNinetyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBfFortyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDZeroThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_CT9H_C.pick())
            self.say(BUILTIN_TEXT_E8IE2J.pick())
            self.memorize_session_then_state(NodeThirtyaStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_8KVRJN.pick())
            self.say(BUILTIN_TEXT_E8IE2J.pick())
            self.memorize_session_then_state(NodeFFortySevenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSeventyThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_1I5JRP.pick())
        self.memorize_session_then_state(NodeBNineFiveStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNineThousandOneHundredAndThirtyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_1I5JRP.pick())
        self.memorize_session_then_state(NodeBNineFiveStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThirtyaStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_KUJFK_.pick())
        self.memorize_session_then_state(NodeNinetyOneeStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFFortySevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_KUJFK_.pick())
        self.memorize_session_then_state(NodeNinetyOneeStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNinetyOneeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_WL84Z8.pick())
        self.memorize_session_then_state(NodeSixThousandAndSixtyNineStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixThousandAndSixtyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEaThirtyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightySevenSevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBNineFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_XXXQV6.pick())
        self.memorize_session_then_state(NodeSixtySevenFourStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixtySevenFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDEightHundredAndFortyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasTakenThompson") is True:
            self.say(BUILTIN_TEXT_HB19NH.pick())
            self.say(BUILTIN_TEXT_ABA5ZI.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreecopyOneStateHandler)
            return self.to_platform_dict()

        elif self.persistent_remember("leoHasSeenThompson") is True:
            self.say(BUILTIN_TEXT_HB19NH.pick())
            self.say(BUILTIN_TEXT_TJKU_X.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreecopyOnecopyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_HB19NH.pick())
            self.say(BUILTIN_TEXT_EDJ_HM.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreecopyStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDEightHundredAndFortyTwocopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasTakenThompson") is True:
            self.say(BUILTIN_TEXT_FU541B.pick())
            self.say(BUILTIN_TEXT_ABA5ZI.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreecopyTwoStateHandler)
            return self.to_platform_dict()

        elif self.persistent_remember("leoHasSeenThompson") is True:
            self.say(BUILTIN_TEXT_FU541B.pick())
            self.say(BUILTIN_TEXT_TJKU_X.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreecopyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_FU541B.pick())
            self.say(BUILTIN_TEXT_EDJ_HM.pick())
            self.say(BUILTIN_TEXT_ZV44QS.pick())
            self.memorize_session_then_state(NodeDSixHundredAndFortyThreeStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNineHundredAndFiftyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_JLCPBB.pick())
        self.say(BUILTIN_TEXT_9YEMYC.pick())
        self.memorize_session_then_state(NodeDThreeTwoStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreecopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreecopyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreecopyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeCOneHundredAndSixtyEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_JLCPBB.pick())
        self.say(BUILTIN_TEXT_9YEMYC.pick())
        self.memorize_session_then_state(NodeDThreeTwoStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeEightyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_JLCPBB.pick())
        self.say(BUILTIN_TEXT_9YEMYC.pick())
        self.memorize_session_then_state(NodeDThreeTwoStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAdEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_SHC3KR.pick())
        self.say(BUILTIN_TEXT_9YEMYC.pick())
        self.memorize_session_then_state(NodeTwoZeroStateHandler)
        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDThreeTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_CWZU_0.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeThreefTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UMHHNE.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeEEightHundredAndFiftyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAFiveHundredAndFortyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_CWZU_0.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeThreefTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UMHHNE.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeEEightHundredAndFiftyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_CWZU_0.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeThreefTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_UMHHNE.pick())
            self.say(BUILTIN_TEXT_SMB32A.pick())
            self.memorize_session_then_state(NodeEEightHundredAndFiftyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreefTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEEightHundredAndFiftyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixThousandSevenHundredAndEighteenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4YPONJ.pick())
            self.say(BUILTIN_TEXT_QAH3W5.pick())
            self.memorize_session_then_state(NodeOnecOneStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBSixHundredAndNinetyEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_4YPONJ.pick())
            self.say(BUILTIN_TEXT_QAH3W5.pick())
            self.memorize_session_then_state(NodeOnecOneStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeHundredAndSixtyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_ADKXX5.pick())
            self.say(BUILTIN_TEXT__OMRE2.pick())
            self.memorize_session_then_state(NodeSixThousandSevenHundredAndEighteenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_7TFTGG.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeFiveThousandOneHundredAndSixtySevenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeHundredAndSixtyCopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.say(BUILTIN_TEXT_SQWO36.pick())
            self.say(BUILTIN_TEXT__OMRE2.pick())
            self.memorize_session_then_state(NodeBSixHundredAndNinetyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_7TFTGG.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeFiveThousandOneHundredAndSixtySevenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeOnecOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_MIBBFS.pick())
            self.memorize_session_then_state(NodeSixHundredAndFiftyStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_ZHTAW1.pick())
            self.memorize_session_then_state(NodeSixHundredAndTwentyFourStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveThousandOneHundredAndSixtySevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreecopyThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDSixHundredAndFortyThreecopyOnecopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.say(BUILTIN_TEXT_HALUVV.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeNineHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        if ShotgunCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VINC3D.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeCOneHundredAndSixtyEightStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_PKNDYS.pick())
            self.say(BUILTIN_TEXT_RPZFTL.pick())
            self.memorize_session_then_state(NodeThreeEightyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenTwentyFourStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.persistent_remember("leoHasChosenWeaponsFirst") is True:
            self.persistent_memorize("leoHasSeenThompson", True)
            self.say(BUILTIN_TEXT_5S3T0_.pick())
            self.say(BUILTIN_TEXT_OY4ICC.pick())
            self.memorize_session_then_state(NodeFZeroZeroStateHandler)
            return self.to_platform_dict()

        else:
            self.persistent_memorize("leoHasSeenThompson", True)
            self.say(BUILTIN_TEXT_ZSIEFU.pick())
            self.say(BUILTIN_TEXT_OY4ICC.pick())
            self.memorize_session_then_state(NodeEightySevenEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightySevenEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_P2E4QQ.pick())
            self.memorize_session_then_state(NodeSevenSevenStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_YLIZXR.pick())
            self.memorize_session_then_state(NodeSevenThousandSixHundredAndSixtyNineStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixteenSixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_HPSFHW.pick())
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeThreeTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeThreeTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBSixHundredAndSeventyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixteenSixcopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_HPSFHW.pick())
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeThreeTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBSixHundredAndSeventyOnecopyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveSevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightyEightThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_2F4_J0.pick())
            self.memorize_session_then_state(NodeSeventyFiveTwoStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_XPRHV9.pick())
            self.memorize_session_then_state(NodeCbbZeroStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeNinetyFourSixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSeventyFiveTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if RifleCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.persistent_memorize("leoHasTakenLeeEndfields", True)
            self.say(BUILTIN_TEXT_RWXHVL.pick())
            self.say(BUILTIN_TEXT_1LUB8N.pick())
            self.memorize_session_then_state(NodeTwentyFoureStateHandler)
            return self.to_platform_dict()

        if ThompsonCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenAPrimaryWeapon", True)
            self.persistent_memorize("leoHasTakenThompson", True)
            self.say(BUILTIN_TEXT_KJWU5Q.pick())
            self.say(BUILTIN_TEXT_1LUB8N.pick())
            self.memorize_session_then_state(NodeFiveHundredAndTwentySixStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_F7D2DK.pick())
            self.say(BUILTIN_TEXT_XPRHV9.pick())
            self.memorize_session_then_state(NodeSevenNineStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeCbbZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VJBSMQ.pick())
            self.memorize_session_then_state(NodeCThreeHundredAndSeventyNineStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_R2FQ5E.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeSixtySevenEightStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwentyFoureStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VJBSMQ.pick())
            self.memorize_session_then_state(NodeCThreeHundredAndSeventyNineStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_MVUC4A.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeEightThousandThreeHundredAndEighteenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiveHundredAndTwentySixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VJBSMQ.pick())
            self.memorize_session_then_state(NodeCThreeHundredAndSeventyNineStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_MVUC4A.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeEightThousandThreeHundredAndEighteenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeCThreeHundredAndSeventyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if ColtCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenColt", True)
            self.say(BUILTIN_TEXT_WNNQHU.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeEightyNineSixStateHandler)
            return self.to_platform_dict()

        if FirstCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenColt", True)
            self.say(BUILTIN_TEXT_WNNQHU.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeEightyNineSixStateHandler)
            return self.to_platform_dict()

        if WebleyCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenWebley", True)
            self.say(BUILTIN_TEXT_PBKMZN.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeAFourHundredAndSeventyTwoStateHandler)
            return self.to_platform_dict()

        if SecondCondition(self).can_handle():
            self.persistent_memorize("leoHasTakenHandPistol", True)
            self.persistent_memorize("leoHasTakenWebley", True)
            self.say(BUILTIN_TEXT_PBKMZN.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeAFourHundredAndSeventyTwoStateHandler)
            return self.to_platform_dict()


    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightThousandThreeHundredAndEighteenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSevenNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_VJBSMQ.pick())
            self.memorize_session_then_state(NodeCThreeHundredAndSeventyNineStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_MVUC4A.pick())
            self.say(BUILTIN_TEXT_9_V_OC.pick())
            self.memorize_session_then_state(NodeEightThousandThreeHundredAndEighteenStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixtySevenEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEightyNineSixStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAFourHundredAndSeventyTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if WithwillieCondition(self).can_handle():
            self.say(BUILTIN_TEXT_JPSUIH.pick())
            self.memorize_session_then_state(NodeDZeroThreeStateHandler)
            return self.to_platform_dict()

        if WithlucCondition(self).can_handle():
            self.say(BUILTIN_TEXT_D5PWFZ.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeSeventyThreeStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_GBDFCV.pick())
            self.say(BUILTIN_TEXT_8PI4BX.pick())
            self.memorize_session_then_state(NodeNineThousandOneHundredAndThirtyOneStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDbfZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeSevenHundredAndFiftyFourStateHandler)
            return self.to_platform_dict()

        else:
            self.say(BUILTIN_TEXT_HPSFHW.pick())
            self.say(BUILTIN_TEXT_GUXF_W.pick())
            self.memorize_session_then_state(NodeThreeTwoStateHandler)
            return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoElevenStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeCbThreeStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass

    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("I have no idea what you want to say")
        return self.to_platform_dict()


def lambda_handler(event, context):
    skill_builder = InoftSkill(settings_yaml_filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.yaml"))
    skill_builder.add_request_handler(EntryRequestHandler)
    skill_builder.add_state_handler(EntryStateHandler)
    skill_builder.add_state_handler(NodeFddTwoStateHandler)
    skill_builder.add_state_handler(NodeCdbSevenStateHandler)
    skill_builder.add_state_handler(NodeNineThousandAndSeventyOneStateHandler)
    skill_builder.add_state_handler(NodeAThirtyFourStateHandler)
    skill_builder.add_state_handler(NodeZeroSixtyEightStateHandler)
    skill_builder.add_state_handler(NodeFortyOneaStateHandler)
    skill_builder.add_state_handler(NodeTwentyThreeSevenStateHandler)
    skill_builder.add_state_handler(NodeFortyEightaStateHandler)
    skill_builder.add_state_handler(NodeNineThousandEightHundredAndThirtyFourStateHandler)
    skill_builder.add_state_handler(NodeSevenEightySevenStateHandler)
    skill_builder.add_state_handler(NodeFFortyEightStateHandler)
    skill_builder.add_state_handler(NodeOneaEightStateHandler)
    skill_builder.add_state_handler(NodeFourHundredAndEightySixStateHandler)
    skill_builder.add_state_handler(NodeENinetyOneStateHandler)
    skill_builder.add_state_handler(NodeAaThreeStateHandler)
    skill_builder.add_state_handler(NodeEdFortyNineStateHandler)
    skill_builder.add_state_handler(NodeSevenHundredAndThirtyThreeStateHandler)
    skill_builder.add_state_handler(NodeSixHundredAndFiftyStateHandler)
    skill_builder.add_state_handler(NodeSixHundredAndTwentyFourStateHandler)
    skill_builder.add_state_handler(NodeSixTwentyStateHandler)
    skill_builder.add_state_handler(NodeSixtyNineEightStateHandler)
    skill_builder.add_state_handler(NodeFZeroZeroStateHandler)
    skill_builder.add_state_handler(NodeThirtyNineEightStateHandler)
    skill_builder.add_state_handler(NodeEightThousandFiveHundredAndSeventyStateHandler)
    skill_builder.add_state_handler(NodeNinetyThreefStateHandler)
    skill_builder.add_state_handler(NodeAdFiveStateHandler)
    skill_builder.add_state_handler(NodeFiveThirtyEightStateHandler)
    skill_builder.add_state_handler(NodeSevenSevenStateHandler)
    skill_builder.add_state_handler(NodeSevenThousandSixHundredAndSixtyNineStateHandler)
    skill_builder.add_state_handler(NodeTwoTwentyOneStateHandler)
    skill_builder.add_state_handler(NodeThreeOneStateHandler)
    skill_builder.add_state_handler(NodeOneHundredAndFortySevenStateHandler)
    skill_builder.add_state_handler(NodeOneHundredAndThirtyThreeStateHandler)
    skill_builder.add_state_handler(NodeFiveThousandFourHundredAndSixteenStateHandler)
    skill_builder.add_state_handler(NodeTwoThousandThreeHundredAndThirtyTwoStateHandler)
    skill_builder.add_state_handler(NodeSixtyEightbStateHandler)
    skill_builder.add_state_handler(NodeFiveHundredAndThirtyFiveStateHandler)
    skill_builder.add_state_handler(NodeThreeThousandThreeHundredStateHandler)
    skill_builder.add_state_handler(NodeFThreeHundredAndSeventyTwoStateHandler)
    skill_builder.add_state_handler(NodeOnebTwoStateHandler)
    skill_builder.add_state_handler(NodeAFiveHundredAndThirtyFiveStateHandler)
    skill_builder.add_state_handler(NodeBcThirtyFiveStateHandler)
    skill_builder.add_state_handler(NodeOneSixtySixStateHandler)
    skill_builder.add_state_handler(NodeSeventyThreeEightStateHandler)
    skill_builder.add_state_handler(NodeSixaThreeStateHandler)
    skill_builder.add_state_handler(NodeOneThousandFiveHundredAndSeventySixStateHandler)
    skill_builder.add_state_handler(NodeSevenHundredAndFiftyFourStateHandler)
    skill_builder.add_state_handler(NodeFourHundredAndTwentyStateHandler)
    skill_builder.add_state_handler(NodeBNineHundredAndNinetyFiveStateHandler)
    skill_builder.add_state_handler(NodeOneThousandSevenHundredAndThirteenStateHandler)
    skill_builder.add_state_handler(NodeTwoHundredAndEightyStateHandler)
    skill_builder.add_state_handler(NodeEightHundredAndNinetyStateHandler)
    skill_builder.add_state_handler(NodeBfFortyTwoStateHandler)
    skill_builder.add_state_handler(NodeDZeroThreeStateHandler)
    skill_builder.add_state_handler(NodeSeventyThreeStateHandler)
    skill_builder.add_state_handler(NodeNineThousandOneHundredAndThirtyOneStateHandler)
    skill_builder.add_state_handler(NodeThirtyaStateHandler)
    skill_builder.add_state_handler(NodeFFortySevenStateHandler)
    skill_builder.add_state_handler(NodeNinetyOneeStateHandler)
    skill_builder.add_state_handler(NodeSixThousandAndSixtyNineStateHandler)
    skill_builder.add_state_handler(NodeEaThirtyFourStateHandler)
    skill_builder.add_state_handler(NodeEightySevenSevenStateHandler)
    skill_builder.add_state_handler(NodeBNineFiveStateHandler)
    skill_builder.add_state_handler(NodeSixtySevenFourStateHandler)
    skill_builder.add_state_handler(NodeDEightHundredAndFortyTwoStateHandler)
    skill_builder.add_state_handler(NodeDEightHundredAndFortyTwocopyStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreeStateHandler)
    skill_builder.add_state_handler(NodeNineHundredAndFiftyFourStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreecopyStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreecopyOneStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreecopyTwoStateHandler)
    skill_builder.add_state_handler(NodeCOneHundredAndSixtyEightStateHandler)
    skill_builder.add_state_handler(NodeThreeEightyOneStateHandler)
    skill_builder.add_state_handler(NodeAdEightStateHandler)
    skill_builder.add_state_handler(NodeDThreeTwoStateHandler)
    skill_builder.add_state_handler(NodeTwoZeroStateHandler)
    skill_builder.add_state_handler(NodeAFiveHundredAndFortyStateHandler)
    skill_builder.add_state_handler(NodeTwoZeroStateHandler)
    skill_builder.add_state_handler(NodeThreefTwoStateHandler)
    skill_builder.add_state_handler(NodeEEightHundredAndFiftyOneStateHandler)
    skill_builder.add_state_handler(NodeSixThousandSevenHundredAndEighteenStateHandler)
    skill_builder.add_state_handler(NodeBSixHundredAndNinetyEightStateHandler)
    skill_builder.add_state_handler(NodeThreeHundredAndSixtyStateHandler)
    skill_builder.add_state_handler(NodeThreeHundredAndSixtyCopyStateHandler)
    skill_builder.add_state_handler(NodeOnecOneStateHandler)
    skill_builder.add_state_handler(NodeFiveThousandOneHundredAndSixtySevenStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreecopyThreeStateHandler)
    skill_builder.add_state_handler(NodeDSixHundredAndFortyThreecopyOnecopyStateHandler)
    skill_builder.add_state_handler(NodeSevenTwentyFourStateHandler)
    skill_builder.add_state_handler(NodeEightySevenEightStateHandler)
    skill_builder.add_state_handler(NodeSixteenSixStateHandler)
    skill_builder.add_state_handler(NodeThreeTwoStateHandler)
    skill_builder.add_state_handler(NodeBSixHundredAndSeventyOneStateHandler)
    skill_builder.add_state_handler(NodeSixteenSixcopyStateHandler)
    skill_builder.add_state_handler(NodeBSixHundredAndSeventyOnecopyStateHandler)
    skill_builder.add_state_handler(NodeFiveSevenStateHandler)
    skill_builder.add_state_handler(NodeEightyEightThreeStateHandler)
    skill_builder.add_state_handler(NodeNinetyFourSixStateHandler)
    skill_builder.add_state_handler(NodeSeventyFiveTwoStateHandler)
    skill_builder.add_state_handler(NodeCbbZeroStateHandler)
    skill_builder.add_state_handler(NodeTwentyFoureStateHandler)
    skill_builder.add_state_handler(NodeFiveHundredAndTwentySixStateHandler)
    skill_builder.add_state_handler(NodeCThreeHundredAndSeventyNineStateHandler)
    skill_builder.add_state_handler(NodeEightThousandThreeHundredAndEighteenStateHandler)
    skill_builder.add_state_handler(NodeSevenNineStateHandler)
    skill_builder.add_state_handler(NodeSixtySevenEightStateHandler)
    skill_builder.add_state_handler(NodeEightyNineSixStateHandler)
    skill_builder.add_state_handler(NodeAFourHundredAndSeventyTwoStateHandler)
    skill_builder.add_state_handler(NodeDbfZeroStateHandler)
    skill_builder.add_state_handler(NodeTwoElevenStateHandler)
    skill_builder.add_state_handler(NodeCbThreeStateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)


if __name__ == "__main__":
    from inoft_vocal_framework.platforms_handlers.simulator.simulator_core import Simulator
    event_, context_ = Simulator(event_type="google/start").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
