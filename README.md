# Inoft Vocal Framework
 ## Create Alexa Skills, Google Actions and Samsung Bixby Capsules with the same codebase. In Python !
 
 #### The example do not show how to deploy the skill (in Lambda, API Gateway and the Javascript files for bixby). I'm soon going to make videos in french and english to explain how to use the framework, and deploy a skill accross platforms. Then a bit later on, there will be the CLI for auto-deployment, then the CMS, then the web interface, then the free cloud platform that will host everything for you while giving you access to everything, then the tools on the platform to collaborate between developpers and voice designers extremly efficiently. It's going to be great ;)
 
 This repo is still under developpement, not everything is implemented. Yet you can see for the dates of releases, it will be soon.
 
 The main framework is constructed, i have build it so that it will be extremly fast and easy to add or change features in the platforms, or even add new platforms !
 
 #### This code makes an Alexa Skill, a Google Action and a Bixby Capsule, and its Pythonic !
 
 Hello World :
 ```
from inoft_vocal_framework import InoftSkill, InoftRequestHandler, InoftDefaultFallback

class LaunchRequestHandler(InoftRequestHandler):
   def can_handle(self) -> bool:
       return self.is_launch_request()

   def handle(self):
       self.say("Hello World !")
       return self.to_platform_dict()

class DefaultFallback(InoftDefaultFallback):
   def handle(self):
       self.say("I did not understand. Do you want for me to say HELLO WORLD ?!")
       return self.to_platform_dict()

def lambda_handler(event, context):
   skill_builder = InoftSkill(disable_database=True)
   skill_builder.add_request_handler(LaunchRequestHandler)
   skill_builder.set_default_fallback_handler(DefaultFallback)
   return skill_builder.handle_any_platform(event=event, context=context)
```
 
 More sophisticated example :
 ```
from inoft_vocal_framework import InoftSkill, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback


class LaunchRequestHandler(InoftRequestHandler):
   def can_handle(self) -> bool:
       return self.is_launch_request()

   def handle(self):
       self.persistent_memorize("has_launched_at_least_once", True)
       self.say("Do you want to read me ? I'm a good example, i assure you !")
       self.memorize_session_then_state(LaunchStateHandler)
       return self.to_platform_dict()

class LaunchStateHandler(InoftStateHandler):
   """ This is a state handler which has been set by the memorize_session_then_state() in the
   LaunchRequestHandler. When the user is in a state_handler, the handler function of the handler
   (for example our Yes and No handlers are not used, and everything is handled by the StateHandler """
   def handle(self):
       """ If something is returned by the handle function (if the user said
       yes or no), we will reset the then_state, and the user can move on """

       # In order for an handler to be used on its own (not in the context of an InoftSkill),
       # you must pass the self keyword to the class. Otherwise you will get an exception.
       if YesHandler(self).can_handle():
           self.say("I'm so happy that you want to read me !")
           return self.to_platform_dict()

       elif NoHandler(self).can_handle():
           self.say("WHAT DO YOU MEAN YOU DO NOT WANT TO READ ME ?!")
           return self.to_platform_dict()

   def fallback(self):
       """ But if nothing is returned, the fallback function is called, and the user will stay in
       the then_state until he said something that will make the handle function return something. """

       self.say("You can say Yes, or No. And that's it my guy")
       return self.to_platform_dict()

class YesHandler(InoftRequestHandler):
   def can_handle(self) -> bool:
       return self.is_in_intent_names(["AMAZON.YesIntent", "OkConfirmation"])

   def handle(self):
       self.persistent_memorize("is_the_user_weird", True)
       self.say(f"Why are you saying Yes ? You are not in a StateHandler. You are crazy weird.")
       return self.to_platform_dict()

class NoHandler(InoftRequestHandler):
   def can_handle(self) -> bool:
       return self.is_in_intent_names(["AMAZON.NoIntent", "NoConfirmation"])

   def handle(self):
       self.say("YOU SAID NO TO ME ?! I KNOW WHERE YOU LIVE !")
       return self.to_platform_dict()

class NumberHandler(InoftRequestHandler):
   def can_handle(self) -> bool:
       return self.is_in_intent_names(["SayANumber"])

   def handle(self):
       # You can get arg_value from intents (slots for Alexa, parameters for Google Assistant and Bixby)
       number = self.get_intent_arg_value(arg_key="number")
       if number is not None:
           self.say(f"Here is your number : {number}")
       else:
           self.say(f"What's your number ? I did not got it.")
       return self.to_platform_dict()

class DefaultFallback(InoftDefaultFallback):
   def handle(self):
       self.say("I have no idea what you want. Go cook yourself an egg.")
       return self.to_platform_dict()


def lambda_handler(event, context):
   # The inoft skill must be initiated in the lambda_handler function, otherwise we would not reset the variables due to staticness of lambda
   skill_builder = InoftSkill(db_table_name="my-table-name_users-data", db_region_name="eu-west-3")
   # For now the framework only support dynamodb as the database client (which is why there is the db_region_name argument)
   skill_builder.add_request_handler(LaunchRequestHandler)
   skill_builder.add_request_handler(YesHandler)
   skill_builder.add_request_handler(NoHandler)
   skill_builder.add_request_handler(NumberHandler)
   skill_builder.add_state_handler(LaunchStateHandler)
   skill_builder.set_default_fallback_handler(DefaultFallback)
   return skill_builder.handle_any_platform(event=event, context=context)
```
 
 ### Roadmap :
 - Redo the README file, and remove the roadmap from it ;)
 - Implement all the available features of Alexa Google Assistant, Samsung Bixby (like all types of cards, carousel, etc)
 - Allow to create +90% of the skill code (Python code of course) with a cartographic (MindMap) tool like the Alexa SkillFlowBuilder.
 - Create a CLI that will automaticly create a AWS lambda, an Alexa Skill, a Google Action, an API Gateway, and link everything together in a few seconds.
 - Create a Content Management/Creation System
 - Make the simulator better and more useful than just sending dumb requests to the code
 - Generate the skill/actions schema right from the code
 - Allow to know on which type of device the user is currently on
 
 ### Already available (the date are the releases date) :
 - Message, and speechs objects helpers (pick according to probability, remember automaticly the last interactions of the user, etc) (a long time ago)
 - Processing and creation of a response (01/28/2020)
 - SkillBuilder and ResponseHandler object to create the response to the intents and requests (01/29/2020)
 - Basic response (speech, ssml, card) (01/29/2020)
 - Processing and manipulating of a request (01/31/2020)
  - Finish the saving of data accross sessions, and make it work when the code is deployed to the cloud (02/17/2020)
 - Micro request simulator (02/01/2020)
 - Identify the intent/request type (like launch, end, and any intent) (02/01/2020)
 - HandlerInput object to have access to all the features without needing 42 imports in each file (02/01/2020)
 - Saving and access of user data/interactions in the session and accross sessions (02/07/2020)
 - StateHandlers (set the user in a state, where he can interacte with multiples intents, and fallback to a specific function if he is not in one of the intents) (02/07/2020)
 - Support basic options of samsung bixby (03/15/2020)
 - Easy handlers to have the messages and speechs in the cloud instead of them being harcoded (is linked with the CMS) (03/07/2020)
 - Allow to have platform specific features in the codebase. For example, in Google Assistant you can have a caroussel, there is no such equivalent in Alexa. (03/08/2020)
 
 #### Credits :
 - The Amazon Alexa Python SDK. If you look at the class and variables that will be interacted with, i have use the same type of logic than the SDK (like a skill_builder, the requests and intents handlers, the handler_input, etc). I did not use their code, but written everything from scratch, unfortunatly ;) https://github.com/alexa/alexa-skills-kit-sdk-for-python
 - The jovo framework. I have taken inspiration of how they handled certains scenarios (like how to save user data accross session in the google assistant). Thank you for being open-source and have clear docs ! https://github.com/jovotech/jovo-framework
