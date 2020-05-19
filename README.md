

# Inoft Vocal Framework

### To allow to make Alexa Skills and Google Actions with ambitions



## Why ?

- We needed a cross platform framework in Python for vocal assistant, it did not exist, we made it.

- We knew we were going to make apps and games that could have big scopes, the techonologies and frameworks allow this did not exist, we made it.

- In order to make sophisticated games, we needed some systems to create content and interactions visually, extend them with ease with full code control, and have a scalable way to audio editing that is re-usable when translating to other languages. We made that to.

  

### In summary

If you are looking to make apps and games on vocal assistants, and might want to make something as simple as a quizz, while knowing that you have in your hand the tools to create a project of any scale and scope. Or if you know that you know right away that you want to do projects with ambitions on vocal assistants. In both cases, the framework that you and us needed did not exist, so we made it.



### The types of peoples this framework is for :

- Technical contractors - Use all of the framework capabilities, the possibility to extends on them and the content creation and management tools to make apps and games that stand out from what most others contractors offers.
- Game developpers - Use the Visual Programming capabilities of the framework, the programmatic audio editing module and the tips on vocal user experience to make an engaging interactive game on vocal assistants available in the documentation. Then, you can use the subscribers management system and the monetisation capabilities to stay fidelise and monetize an audience.
- Web & Mobiles Apps developpers - Use the intent and event based that works similarly to a website or an app backend, coupled with the content management system and the tips on how on how to use experience in web and mobile development on vocal assistants development, to make compelings apps that you can market.
- Marketing contractors - Use the easy to use content management system, Visual Programming tools and subscribers management system to allow to create a new connection trough a novel experience for the users and clients of the companies you are working with.k

### The types of peoples this framework is NOT for:

- Non-technical writters & designers - Even if you can develop an interactive story without touching a line of code, you will need to get your hands dirty with the deployment, the setting up and publication of your apps, etc. If you have no technical experience, if you are eager to learn, it might take you a week or two before becoming with using the framework (less if you are only using Visual Development)





#### Requirements :

- An AWS (Amazon Web Services) account (you can create one with your Amazon account) (https://aws.amazon.com/)
- Python (3.6 minimum, 3.7.+ highly recommanded, the 3.8.X versions might work yet have not been tested) (https://www.python.org/downloads/)
- (In order to create an Alexa Skill) An Amazon developer account (takes 20 seconds to create) https://developer.amazon.com/fr/
- (In order to create a Google Assistant Action) A Google Account (you use your regular Google/Gmail account as your developer account) https://developers.google.com/assistant



### Installation (Python 3.7 is recommanded. Python 3.6+ is required) :

```
 pip install inoftvocal
```

### Usage :

#### After installation, open a terminal (cmd), then start a project with the command

```
 inoft new
```

 You will have to select a folderpath in which your project will be created, and select a template to start with. You can then use your favorite code editor to open the folder containing your newly created project.

#### Deploying to AWS

```
 inoft deploy
```



#### Hello World Example :

```python
class LaunchRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
       return self.is_launch_request()
    
    def handle(self):
       self.say("Hello world ! I hope you are doing great ! Bye !")
       self.end_session()
       return self.to_platform_dict()
       
# A class to handle the default response of the app is always required.
class DefaultFallback(InoftDefaultFallback):
   def handle(self):
       self.say("I did not understand... Goodbye...")
       self.end_session()
       return self.to_platform_dict()

# This function is called by our serverless service (like AWS Lamda) on every interaction of an user with our app.
def lambda_handler(event, context):
   skill_builder = InoftSkill(disable_database=True)
   skill_builder.add_request_handler(LaunchRequestHandler)
   skill_builder.set_default_fallback_handler(DefaultFallback)
   return skill_builder.handle_any_platform(event=event, context=context)
   
# For local development and testing, we use the simulator module
if __name__ == "__main__":
    from inoft_vocal_framework import Simulator
    event_, context_ = Simulator(platform=Simulator.PLATFORM_GOOGLE, event_type="launch").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
```





#### Unique Points

| Name                                                        | Description                                                  |
| :---------------------------------------------------------- | :----------------------------------------------------------- |
| Cross-Platform with all platforms specific functionnalities | Depeding on your application, around 80-95% of your code will be shared for all platforms (Alexa, Google Assistant, and soon Siri and Samsung Bixby), all the while having access to all of the platforms specifics features. |
| Made in Python                                              | Do not limit yourself to small projects, by using all of your classical Python librairies and the Python syntax suitable for projects of any size. |
| AWS Optimized                                               | Take full advantage of the AWS services, like the latest and fastest HTTP API'S, or possibility to have your database clients be static on AWS Lambda to provide a response time that can be up to 20x faster than classic librairies. |
| Serverless Architecture                                     | Made to be used with a serverless architecture (like AWS Lambda), so that you only pay for what you use, and do not face any scabilities issues. |
| Made to be robust and pereine                               | In the way it has been designed, and the way it deploy the version you used for your application, the framework has been made with the goal of pereinity of the applications in mind. |
| Fully Open-Source under the MIT License                     | You can do anything you want with the framework. Use it in your projects, modify it, sell it without even modifying it. The MIT License give you a total freedom. |
| Made to allow projects of large scales                      | Unlike the others few libraries, the way the framework allows your code to be structured has been made to enable something as simple as a quizz, or an interactive game that take 200 hours to play. |



#### Basic Concepts

| Name                               | Description                                                  | Available          |
| :--------------------------------- | :----------------------------------------------------------- | :----------------- |
| Auto-deployment                    | Automaticly deploy your applications and contents to AWS with the command line interface and create a light weight package with all of the librairies available in the cloud | :white_check_mark: |
| Modular Logic                      | No matter the size, keep the code of your project clear, with five différents modular classes that you can use to handle the logic of your application. | :white_check_mark: |
| Intent Handling                    | Easy way to provide different responses to the users according to their intents (saying "I need a booking", and "Can you give me a booking ?" put the user in the same intent that you could call wantBooking) | :white_check_mark: |
| Data Input                         | Retrieve parameters that the user has specified, for example, "We will be 3 players", you could retrieve the number of players. | :white_check_mark: |
| Choices States                     | Easily put your user in a state with multiple choices and saying an helpful message if the user has not chosen one of the available choicex | :white_check_mark: |
| Visual Elements with errors checks | Display any visual elements on Amazon Alexa and Google Assistant (that will be available on devices with screens) with built-in checks and errors to make sure your elements respect the platforms constraints (instead of your application not working without any errors) | :white_check_mark: |



#### Advanced Features

| Name                                                 | Description                                                  | Available          |
| :--------------------------------------------------- | :----------------------------------------------------------- | :----------------- |
| Notifications subscribers management system          | Easily organize the users that have subscribed to receive notifications in groups in a similar way to a newsletter management system | Next version       |
| Speech Builder                                       | Easily create SSML responses to provide variety and more customizations to your syntheied speechs responses. | :white_check_mark: |
| Smart Sessions & Automatic State Resuming            | Instead of ending an user session when the application is closed (intentionnaly or by mistake) define a timeout (for example 60 seconds) that if not crossed since the last use of the application will resume the user previous session attributes and where he was in the application (or ask him if he want to resume), with zero line of code required on your side. | :white_check_mark: |
| Functional Callbacks for interactive Visual Elements | When creating a Visual Elements that the user can interact with, provide your callback functions for the different scenarios right when creating the elements (instead of needing to create a whole conditionnal id based system for each interactive element) | :white_check_mark: |



#### Programmatic Audio Editing

| Name                                             | Description                                                  | Available             |
| :----------------------------------------------- | :----------------------------------------------------------- | :-------------------- |
| Track based system                               | Unlimited liberty to make your sounds by using the same methods as professional manual audio editing software. | :white_check_mark:    |
| Automatic upload of your files                   | Just use the local path to your source audio files, all the tedious work of formatting and uploading your sources and generated files will be done automaticly for you. | :black_square_button: |
| Make your audio content as robust as code        | Instead of facing the hasle of updating or translating audio files that have been created in an external audio software, create, combine, modify and update your audio content programatictly. | :white_check_mark:    |
| Relations system between your sounds             | Need to have a gun shot start half a second after a character has finished speaking ? Use a relation between the two sounds. No additionnal work will be needed if you change the character speech, or if you make a translation of it that is of a different duration. | :white_check_mark:    |
| Do not limit your use of sophisticated scenarios | Instead of giving up having a lot of possibilities for the user when using recorded audio because of the complexity of creating all of the audio files, you can easily combine multiple audio files and use the same ambiances, transitions, etc on all of your combinaisons. | :white_check_mark:    |



#### Visual Programming

| Name                        | Description                                                  | Available             |
| :-------------------------- | :----------------------------------------------------------- | :-------------------- |
| Botpress integration        | Use Botpress, an open-source tool (with over height thousands stars on GitHub) that has been designed to make textual chatbot, to now make your interactions heavy projects on vocal assistants | :white_check_mark:    |
| Generate everything         | From your code logic, your content, to your interactions models, you can design everything in Botpress and generate all of the code for vocal assistants while having access to all of the framework capabilities. | :black_square_button: |
| Generate readable code      | We have put the emphasis on making the code generation more readable and navigable than human code, so that will always have the hand on your code so that you can extend on it anyway you like. | :white_check_mark:    |
| Extends the code generation | Need to use visual programming for a big project that cannot be done with manual code, yet you have created some uniques fonctionnalities or logic that you want to use without destroying your CTRL-V key each time you re-generate the code ? You can easily create an extension for the code/content/models generation by customizing the framework Jinja2 templates or by creating new ones. | :black_square_button: |





#### Credits :

- The Alexa Python SDK (https://github.com/alexa/alexa-skills-kit-sdk-for-python). I have taken a big inspiration on how they to decided to make the interaction with the framework, for example trough class that have a can_handle and handle function.
- The Jovo framework (https://github.com/jovotech/jovo-framework) I have taken inspiration of how they handled certains scenarios (like how to save user data accross session in the google assistant).
- The Zappa package (https://github.com/Miserlou/Zappa). I have used the code of the package as an inspiration and a starting point to create the auto-deployement.
- The BotPress project, in my opinion the most powerful bot building tool, to which the Inoft Vocal Framework has an integration in order to use it with vocal assistants (https://github.com/botpress/botpress)
