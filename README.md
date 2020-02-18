# Inoft Vocal Framework
 ## Create Alexa Skills and Google Actions with the same codebase. In Python !
 
 
 This repo is still under developpement, not everything is implemented. Yet you can see for the dates of releases, it will be soon.
 
 The main framework is constructed, i have build it so that it will be extremly fast and easy to add or change features in the platforms, or even add new platforms !
 
 #### This code makes both an Alexa Skill and a Google Action, and its Pythonic !
 
 ```
 class LaunchRequestHandler(InoftRequestHandler):
    def can_handle(self):
        return self.is_launch_request()

    def handle(self):
        self.persistent_memorize("has_launched_at_least_once", True)
        self.session_memorize("count_interactions_in_session", 1)
        
        self.say("Readme, readme, readme... README !")
        return self.to_platform_dict()
        
class YesHandler(InoftRequestHandler):
    DEFAULT_YES_INTENT_NAME = "AMAZON.YesIntent"
    CUSTOM_OK_INTENT_NAME = "OkConfirmation"

    def can_handle(self):
        return self.is_in_intent_names([self.DEFAULT_YES_INTENT_NAME, self.CUSTOM_OK_INTENT_NAME])

    def handle(self):
        self.say("Im currently implementing the system to handle easily the previous interactions."
                 "Yet we can at least manipulate some informations !")
                 
        self.session_memorize("count_interactions_in_session",
                              self.session_remember("count_interactions_in_session", int) + 1)

        return self.to_platform_dict()
        
skill_builder = InoftSkill()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(YesHandler())

def lambda_handler(event, context):
    return handle_any_platform(event=event, context=context, skill_builder=skill_builder)
```
 
 ### Roadmap :
 - Implement all the available features of Alexa and Google Assistant (like cards, carousel, etc)
 - Allow to have platform specific features in the codebase. For example, in Google Assistant you can have a caroussel, there is no such equivalent in Alexa.
 - Allow to create +90% of the skill code (Python code of course) with a cartographic (MindMap) tool like the Alexa SkillFlowBuilder.
 - Create a CLI that will automaticly create a AWS lambda, an Alexa Skill, a Google Action, an API Gateway, and link everything together in a few seconds.
 - Create a Content Management/Creation System
 - Make the simulator better and more useful than just sending dumb requests to the code
 - Generate the skill/actions schema right from the code
 - Easy handlers to have the messages and speechs in the cloud instead of them being harcoded (is linked with the CMS)
 - Support samsung bixby
 
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
 
 #### Credits :
 - The Amazon Alexa Python SDK. If you look at the class and variables that will be interacted with, i have use the same type of logic than the SDK (like a skill_builder, the requests and intents handlers, the handler_input, etc). I did not use their code, but written everything from scratch, unfortunatly ;) https://github.com/alexa/alexa-skills-kit-sdk-for-python
 - The jovo framework. I have taken inspiration of how they handled certains scenarios (like how to save user data accross session in the google assistant). Thank you for being open-source and have clear docs ! https://github.com/jovotech/jovo-framework
