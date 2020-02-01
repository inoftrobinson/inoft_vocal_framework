# inoft_vocal_framework
 Create Alexa Skills and Google Action with the same codebase. In Python !
 
 
 This repo is still under developpement, not everything is implemented. Yet you can see for the dates of releases, it will be soon.
 
 The main framework is constructed, i have build it so that it will be extremly fast and easy to add or change features in the platforms, or even add new platforms !
 
 
 Roadmap :
 - Saving and access of user data/interactions in the session and accross sessions
 - Implement all the available features of Alexa and Google Assistant
 - Allow to have platform specific features in the codebase. For example, in Google Assistant you can have a caroussel, there is no such equivalent in Alexa.
 - Allow to create +90% of the skill code (Python code of course) with a cartographic (MindMap) tool like the Alexa SkillFlowBuilder.
 
 Already available (the date are the releases date) :
 - Message, and speechs objects helpers (pick according to probability, remember automaticly the last interactions of the user, etc) (a long time ago)
 - Processing and creation of a response (01/28/2020)
 - SkillBuilder and ResponseHandler object to create the response to the intents and requests (01/29/2020)
 - Basic response (speech, ssml, card) (01/29/2020)
 - Processing and manipulating of a request (01/31/2020)
 - Identify the intent/request type (like launch, end, and any intent) (02/01/2020)
 - HandlerInput object to manipulate everything without needing 42 imports in each file (02/01/2020)
