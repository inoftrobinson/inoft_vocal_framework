# Inoft Vocal Framerwork
 ## Create Alexa Skills and Google Actions with the same codebase. In Python !
 
 
 This repo is still under developpement, not everything is implemented. Yet you can see for the dates of releases, it will be soon.
 
 The main framework is constructed, i have build it so that it will be extremly fast and easy to add or change features in the platforms, or even add new platforms !
 
 #### This code makes both an Alexa Skill and a Google Action, and its Pythonic !
 
 ```
 class LaunchRequestHandler(InoftRequestHandler):
    KEY_REQUEST_INTERACTION_TYPE = "LaunchRequest"

    def can_handle(self, handler_input: HandlerInput):
        return handler_input.is_launch_request()

    def handle(self, handler_input: HandlerInput):
        output_response = response_factory.Response()
        output_response.outputSpeech.set_ssml(MSGS_FIRST_USE_WELCOME.pick(handler_input))
        return output_response.to_platform_dict()
        
skill_builder = InoftSkill()
skill_builder.add_request_handler(LaunchRequestHandler())

def lambda_handler(event, context):
    return handle_any_platform(event=event, context=context, skill_builder=skill_builder)
```
 #### What this code is doing :
 - Create an Handler for the launch of the skill/action.
 - Defince under which conditions this should be the handler to be used (with the can_handle function)
 - Processing an Alexa or a Google Assistant request (and finding out who is calling it)
 
 
 ### Roadmap :
 - Saving and access of user data/interactions in the session and accross sessions
 - Implement all the available features of Alexa and Google Assistant
 - Allow to have platform specific features in the codebase. For example, in Google Assistant you can have a caroussel, there is no such equivalent in Alexa.
 - Allow to create +90% of the skill code (Python code of course) with a cartographic (MindMap) tool like the Alexa SkillFlowBuilder.
 - Create a CLI that will automaticly create a AWS lambda, an Alexa Skill, a Google Action, an API Gateway, and link everything together in a few seconds.
 
 ### Already available (the date are the releases date) :
 - Message, and speechs objects helpers (pick according to probability, remember automaticly the last interactions of the user, etc) (a long time ago)
 - Processing and creation of a response (01/28/2020)
 - SkillBuilder and ResponseHandler object to create the response to the intents and requests (01/29/2020)
 - Basic response (speech, ssml, card) (01/29/2020)
 - Processing and manipulating of a request (01/31/2020)
 - Identify the intent/request type (like launch, end, and any intent) (02/01/2020)
 - HandlerInput object to have access to all the features without needing 42 imports in each file (02/01/2020)
 
 #### Credits :
 - The Amazon Alexa Python SDK. If you look at the class and variables that will be interacted with, i have use the same type of logic than the SDK (like a skill_builder, the requests and intents handlers, the handler_input, etc). I did not use their code, but written everything from scratch, unfortunatly ;)
