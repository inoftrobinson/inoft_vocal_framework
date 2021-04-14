from json import dumps as json_dumps
from typing import Optional, List

from pydantic import Field, PrivateAttr
from pydantic.main import BaseModel

from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict

# todo: add select carousel
# todo: add select list

class OpenUrlAction(BaseModel):
    url: str

class Image(BaseModel):
    url: str
    accessibilityText: str

class ImageDisplayOptions(BaseModel):
    _CROPPED_TYPE = "CROPPED"
    _AVAILABLE_OPTIONS_TYPES = [_CROPPED_TYPE]

    option_type: str

class Button(BaseModel):
    title: str = ""
    openUrlAction: str = ""

class BasicCard(BaseModel):
    title: str
    subtitle: str
    formattedText: Optional[str] = None
    buttons: Optional[List[Button]] = None
    image: Optional[Image] = None
    imageDisplayOptions: Optional[ImageDisplayOptions] = None

    def return_transformations(self) -> None:
        self.imageDisplayOptions = self.imageDisplayOptions if self.imageDisplayOptions is None else self.imageDisplayOptions.option_type


# todo: check if an image/video url is valid and throw an exception if not
# todo: raise for google if more than 2 response items have been set
# todo: do not allow to use elements that the plateform cannot support (like a carousel need to be on a platform that support a web browser, like a phone)

class BrowseCarousel(BaseModel):
    class CarouselItemModel(BaseModel):
        title: str
        description: Optional[str] = None
        image: Optional[Image] = None
        openUrlAction: Optional[OpenUrlAction] = None
        footer: Optional[str] = None
    items: List[CarouselItemModel] = Field(default_factory=list)
    _first_item_used_keys: Optional[List[str]] = PrivateAttr(default=None)

    def add_item(
            self, title: str, url_to_open_on_click: str, description: str = None,
            image_url: str = None, image_accessibility_text: str = None, footer: str = None
    ):
        if len(self.items) < 10:
            # A carousel can have a maximum of 10 items
            item = self.CarouselItemModel(
                title=title, description=description, openUrlAction=OpenUrlAction(url=url_to_open_on_click), footer=footer,
                image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text)
            )
            if self._first_item_used_keys is None:
                self._first_item_used_keys = ['title', 'url_to_open_on_click']
                if description is not None:
                    self._first_item_used_keys.append('description')
                if image_url is not None:
                    self._first_item_used_keys.append('image_url')
                if image_accessibility_text is not None:
                    self._first_item_used_keys.append('image_accessibility_text')
                if footer is not None:
                    self._first_item_used_keys.append('footer')
            else:
                if (('description' in self._first_item_used_keys if description is None else 'description' not in self._first_item_used_keys)
                or ('image_url' in self._first_item_used_keys if image_url is None else 'image_url' not in self._first_item_used_keys)
                or ('image_accessibility_text' in self._first_item_used_keys if image_accessibility_text is None else 'image_accessibility_text' not in self._first_item_used_keys)
                or ('footer' in self._first_item_used_keys if footer is None else 'footer' not in self._first_item_used_keys)):
                    raise Exception(f"All carousel items must have the same variable, to assure a tile consistency."
                                    f"The first item of the carousel had the following variables : {self._first_item_used_keys}"
                                    f"which are not the same as the last item you inserted : {item.__dict__}")

            self.items.append(item)
        else:
            print("The browse carousel items limit of 10 has ben reached. Your new item has not been included.")

    def do_not_include(self):
        # If no items are present in the carousel, we do not include it
        return len(self.items) == 0

    def return_transformations(self) -> None:
        if self.do_not_include() is False and len(self.items) == 1:
            # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
            first_item = self.items[0]
            if isinstance(first_item, self.CarouselItemModel):
                self.items.append(self.CarouselItemModel(
                    title=first_item.title, description=first_item.description, image=first_item.image,
                    openUrlAction=first_item.openUrlAction, footer=first_item.footer
                ))
                print(f"Warning, a carousel had only one item, since we require two items, the only one has been duplicated.")
            else:
                raise Exception(f"The first_item of the carousel was not an instance of carousel item but {first_item}")


class MediaResponse(BaseModel):
    _KEY_MEDIA_TYPE_AUDIO = "AUDIO"

    # todo: check that the user device has the capability to play audio files in a media response
    # todo: add follow up when audio file has finished playing

    mediaType: Optional[_KEY_MEDIA_TYPE_AUDIO] = Field(default=_KEY_MEDIA_TYPE_AUDIO)
    class MediaObject(BaseModel):
        contentUrl: str
        name: str
        description: Optional[str] = None
        icon: Optional[Image] = None
    mediaObjects: List[MediaObject] = Field(default_factory=list)

    def add_audio_content(
            self, mp3_file_url: str, name: str, description: str = None,
            icon_image_url: str = None, icon_accessibility_text: str = None
    ):
        # todo: check validity of mp3 file, otherwise print a warning and do not add the item
        #  (and if it was the only item, do not include the media response)

        if self.mediaType is None:
            self.mediaType = self._KEY_MEDIA_TYPE_AUDIO
        else:
            if self.mediaType != self._KEY_MEDIA_TYPE_AUDIO:
                raise Exception(f"You cannot add an audio content object if you have already instantiated a media"
                                f"object by adding a different content that is of media type {self.mediaType}")

        self.mediaObjects.append(self.MediaObject(
            content_url=mp3_file_url, name=name, description=description,
            icon=None if icon_image_url is None else Image(image_url=icon_image_url, accessibility_text=icon_accessibility_text))
        )


class SystemIntent(BaseModel):
    _INTENT_TYPE_OPTION = "actions.intent.OPTION"
    _INTENT_TYPE_PERMISSION = "actions.intent.PERMISSION"
    _AVAILABLE_INTENT_KEYS_TYPES = [_INTENT_TYPE_OPTION, _INTENT_TYPE_PERMISSION]
    _ELEMENT_TYPE_LIST_SELECT = "ListSelect"
    _ELEMENT_TYPE_CAROUSEL_SELECT = "CarouselSelect"
    _ELEMENT_TYPE_ASK_PERMISSION = "AskPermission"
    _OPTION_ELEMENTS_TYPES_KEYS = [_ELEMENT_TYPE_LIST_SELECT, _ELEMENT_TYPE_CAROUSEL_SELECT]
    _PERMISSION_ELEMENTS_TYPES_KEYS = [_ELEMENT_TYPE_ASK_PERMISSION]

    intent: str
    class Data(BaseModel):
        type: str = Field(alias='@type')

        class InteractiveListOrCarouselItemModel(BaseModel):
            title: str
            description: Optional[str] = None
            image: Optional[Image] = None

            class OptionInfo(BaseModel):
                key: str
                synonyms: List[str] = Field(default_factory=list)

                def __init__(self, identifier_key: str):
                    import random  # todo: check if synonyms are required and add possibility to set them
                    super().__init__(key=identifier_key, synonyms=[f"{random.randint(0, 1000000000000000)}"])
            optionInfo: Optional[OptionInfo] = None

            def __init__(self, identifier_key: str, **kwargs):
                super().__init__(optionInfo=self.OptionInfo(identifier_key=identifier_key), **kwargs)

        class ListSelectModel(BaseModel):
            title: str
            items: list

            def add_item(
                    self, identifier_key: str, title: str, description: str = None,
                    image_url: str = None, image_accessibility_text: str = None
            ):

                if len(self.items) < 30:
                    self.items.append(SystemIntent.Data.InteractiveListOrCarouselItemModel(
                        identifier_key=identifier_key, title=title, description=description,
                        image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text))
                    )
                else:
                    print("The list items limit of 30 has ben reached. Your new item has not been included.")

            def do_not_include(self):
                # If no items are present in the list, we do not include it
                return len(self.items) == 0

            def return_transformations(self) -> None:
                if self.do_not_include() is False and len(self.items) == 1:
                    # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
                    first_item = self.items[0]
                    if isinstance(first_item, SystemIntent.Data.InteractiveListOrCarouselItemModel):
                        new_identifier_key = f"{first_item.optionInfo.key}.2"
                        self.items.append(SystemIntent.Data.InteractiveListOrCarouselItemModel(
                            identifier_key=new_identifier_key, title=f"2 - {first_item.title}",
                            description=first_item.description, image=first_item.image))

                        first_item.title = f"1 - {first_item.title}"
                        print(f"Warning, a list had only one item, since we require two items, the only one has been duplicated"
                              f"with a new id of {new_identifier_key} instead of dumbly duplicating the id {first_item.optionInfo.key}"
                              f"A '1 -' and a '2 -' have also been added to the elements titles, to make them both uniques.")
                    else:
                        raise Exception(f"The first_item of the list was not an instance of list item but {first_item}")
        listSelect: Optional[ListSelectModel] = None

        class CarouselSelectModel(BaseModel):
            items: list

            def add_item(
                    self, identifier_key: str, title: str, description: str,
                    image_url: str = None, image_accessibility_text: str = None
            ):
                if len(self.items) < 10:
                    self.items.append(SystemIntent.Data.InteractiveListOrCarouselItemModel(
                        identifier_key=identifier_key, title=title, description=description,
                        image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text))
                    )
                else:
                    print("The carousel items limit of 10 has ben reached. Your new item has not been included.")

            def do_not_include(self):
                # If no items are present in the carousel, we do not include it
                return len(self.items) == 0

            def return_transformations(self) -> None:
                if self.do_not_include() is False and len(self.items) == 1:
                    # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
                    first_item = self.items[0]
                    if isinstance(first_item, SystemIntent.Data.InteractiveListOrCarouselItemModel):
                        new_identifier_key = f"{first_item.optionInfo.key}.2"
                        self.items.append(SystemIntent.Data.InteractiveListOrCarouselItemModel(
                            identifier_key=new_identifier_key, title=f"2 - {first_item.title}",
                            description=first_item.description, image=first_item.image))

                        first_item.title = f"1 - {first_item.title}"
                        print(f"Warning, a list had only one item, since we require two items, the only one has been duplicated"
                              f"with a new id of {new_identifier_key} instead of dumbly duplicating the id {first_item.optionInfo.key}"
                              f"A '1 -' and a '2 -' have also been added to the elements titles, to make them both uniques.")
                    else:
                        raise Exception(f"The first_item of the list was not an instance of list item but {first_item}")
        carouselSelect: Optional[CarouselSelectModel] = None

        permissions: Optional[List[str]] = None

        class UpdatePermissionValueSpecModel(BaseModel):
            intent: str
        updatePermissionValueSpec: Optional[UpdatePermissionValueSpecModel] = None

        def __init__(self, element_type: str, permissions_update_intent_name: Optional[str] = None):
            kwargs = {}
            if element_type == SystemIntent._ELEMENT_TYPE_LIST_SELECT:
                kwargs['@type'] = "type.googleapis.com/google.actions.v2.OptionValueSpec"
                kwargs['listSelect'] = self.ListSelectModel()
            elif element_type == SystemIntent._ELEMENT_TYPE_CAROUSEL_SELECT:
                kwargs['@type'] = "type.googleapis.com/google.actions.v2.OptionValueSpec"
                kwargs['carouselSelect'] = self.CarouselSelectModel()
            elif element_type == SystemIntent._ELEMENT_TYPE_ASK_PERMISSION:
                if permissions_update_intent_name is None:
                    raise Exception(f"The intent_name argument in the request_push_notifications_permission_if_missing function has not been defined.")
                kwargs['@type'] = "type.googleapis.com/google.actions.v2.PermissionValueSpec"
                kwargs['permissions'] = ['UPDATE']
                kwargs['updatePermissionValueSpec'] = self.UpdatePermissionValueSpecModel(intent=permissions_update_intent_name)
            else:
                raise Exception(f"The element_type {element_type} is not a supported element type.")
            super().__init__(**kwargs)

        """def return_transformations(self):
            # The key that google is expecting is the @type key, yet since in python i cannot directly set a variable
            # with the @type name, we use a simple '_type' variable name, and in the return transformations, we create
            # a new var called '@type' with the vars dict to which we assign the value of the 'type' property (it points
            # to the '_type' variable) and then we can delete the '_type' variable to not include it in the output dict.
            vars(self)["@type"] = self.type
            del self._type"""

    data: Data

    def __init__(self, element_type: str, permissions_update_intent_name: Optional[str] = None):
        if element_type in self._OPTION_ELEMENTS_TYPES_KEYS:
            intent = self._INTENT_TYPE_OPTION
        elif element_type in self._PERMISSION_ELEMENTS_TYPES_KEYS:
            intent = self._INTENT_TYPE_PERMISSION
        else:
            raise Exception(f"The element_type '{element_type}' for the SystemIntent as not been recognized.")

        data = self.Data(element_type=element_type, permissions_update_intent_name=permissions_update_intent_name)
        super().__init__(intent=intent, data=data)

class SimpleResponse(BaseModel):
    textToSpeech: str = ""
    displayText: str = ""


class RichResponseInPayload(BaseModel):
    items: list = Field(default_factory=list)
    suggestions: list = Field(default_factory=list)

    def add_response_item(self, response_item_object) -> int:
        """:return Length of the list containing all the response items"""
        self.items.append(response_item_object)
        return len(self.items) - 1

    def add_suggestion_chip(self, title: str):
        # todo: add external link suggestion chip (cannot be used on platforms without the actions.capability.WEB_BROWSER capability
        if not isinstance(title, str):
            raise Exception(f"The title variable must be of type str but was {type(title)}")
        if len(title) > 25:
            raise Exception(f"A suggestion chip title can have a maximum of 25 chars but {title} was {len(title)} chars")

        self.suggestions.append({"title": title})

    def return_transformations(self):
        for i in range(len(self.items)):
            self.items[i] = NestedObjectToDict.get_dict_from_nested_object(
                object_to_process=self.items[i], key_names_identifier_objects_to_go_into=["json_key"]
            )


class GoogleInPayload(BaseModel):
    expectUserResponse: bool = True
    richResponse: RichResponseInPayload = Field(default_factory=RichResponseInPayload)
    userStorage: str = ""
    systemIntent: Optional[SystemIntent] = None


class Payload(BaseModel):
    google: GoogleInPayload = Field(default_factory=GoogleInPayload)

class OutputContextItem(BaseModel):
    _SESSION_DATA_NAME = "sessionData"

    name: str
    lifespanCount: int
    parameters: dict = Field(default_factory=dict)

    def __init__(self, session_id: str, name: str, lifespanCount=999):
        name = f"{session_id}/contexts/{name}"
        super().__init__(name=name, lifespanCount=lifespanCount)

    def return_transformations(self) -> None:
        if "data" in self.parameters.keys():
            self.parameters["data"] = json_dumps(self._parameters["data"])

    def add_set_parameter(self, parameter_key: str, parameter_value=None):
        """
        :param parameter_key: str key for the parameters dict object, should not be an empty str
        :param parameter_value: any object, cannot be None
        :return: self
        """
        if parameter_value is not None and isinstance(parameter_key, str) and parameter_key != "":
            self.parameters[parameter_key] = parameter_value
        return self

    def add_set_session_attribute(self, parameter_key: str, parameter_value=None):
        if "data" not in self.parameters.keys():
            self.parameters["data"] = dict()

        if parameter_value is not None and isinstance(parameter_key, str) and parameter_key != "":
            self.parameters["data"][parameter_key] = parameter_value
        return self


class Response(BaseModel):
    payload: Payload = Field(default_factory=Payload)
    outputContexts: list = Field(default_factory=list)
    _first_say_rich_response_list_id: Optional[int] = PrivateAttr(default=None)
    _second_say_rich_response_list_id: Optional[int] = PrivateAttr(default=None)

    def say(self, text_or_ssml: str) -> None:
        # todo: allow to have 2 differents response in the same one, not just one (the textToSpeech and the displayText)
        if self._first_say_rich_response_list_id is None:
            output_response = SimpleResponse()
            output_response.textToSpeech = text_or_ssml
            output_response.displayText = "displayText"
            self._first_say_rich_response_list_id = self.payload.google.richResponse.add_response_item(output_response)
        else:
            self.payload.google.richResponse.items[self._first_say_rich_response_list_id].textToSpeech += ("\n" + text_or_ssml)

    def second_say(self, text_or_ssml: str) -> None:
        if self._second_say_rich_response_list_id is None:
            output_response = SimpleResponse()
            output_response.textToSpeech = text_or_ssml
            self._second_say_rich_response_list_id = self.payload.google.richResponse.add_response_item(output_response)
        else:
            self.payload.google.richResponse.items[self._second_say_rich_response_list_id].textToSpeech += ("\n" + text_or_ssml)

    def say_reprompt(self, text_or_ssml: str) -> None:
        # todo: finish the reprompt function
        return None
        output_response = SimpleResponse()
        output_response.textToSpeech = text_or_ssml
        self.payload.google.richResponse.add_response_item(output_response)

    def end_session(self, should_end: bool = True) -> None:
        self.payload.google.expectUserResponse = False if should_end is True else True

    def add_output_context_item(self, output_context_item: OutputContextItem) -> None:
        if isinstance(output_context_item, OutputContextItem):
            self.outputContexts.append(output_context_item)
        else:
            raise Exception(f"The output context item needed to be of instance {OutputContextItem} but was : {output_context_item}")

    def add_response_item_to_show(self, item_object) -> None:
        if not len(self.payload.google.richResponse.items) > 0:
            raise Exception("A google response take in consideration the order with which the elements have been added. "
                            "You cannot set a visual element as first element of the response. "
                            "Try to set a speech element with the .say() function before you add a visual element.")
        self.payload.google.richResponse.add_response_item(item_object)

    def add_suggestions_chips(self, chips_titles: list) -> None:
        if isinstance(chips_titles, list):
            for chip_title in chips_titles:
                self.payload.google.richResponse.add_suggestion_chip(title=chip_title)
        elif isinstance(chips_titles, str):
            self.payload.google.richResponse.add_suggestion_chip(title=chips_titles)

    def add_item_to_browse_carousel(
            self, title: str,  url_to_open_on_click: str, description: str = None,
            image_url: str = None, image_accessibility_text: str = None, footer: str = None
    ) -> None:
        carousel_instance = None
        # todo: improve this loop so that we do not need to loop every time we add an item
        for response_item in self.payload.google.richResponse.items:
            if isinstance(response_item, BrowseCarousel):
                carousel_instance = response_item
                break
        if carousel_instance is None:
            carousel_instance = BrowseCarousel()
            self.payload.google.richResponse.items.append(carousel_instance)
        carousel_instance.add_item(
            title=title, url_to_open_on_click=url_to_open_on_click, description=description,
            image_url=image_url, image_accessibility_text=image_accessibility_text, footer=footer
        )

    def add_interactive_list_item_to_system_intent(
            self, identifier_key: str, item_title: str, item_description: str = None,
            item_image_url: str = None, item_image_accessibility_text: str = None
    ) -> None:
        if 'systemIntent' not in vars(self.payload.google):
            self.payload.google.systemIntent = SystemIntent(element_type=SystemIntent._ELEMENT_TYPE_LIST_SELECT)
        elif self.payload.google.systemIntent.data.listSelect is None:
            # If the listSelect variable is None, it means that the SystemIntent do not represent a ListSelect,
            # and an exception will be thrown (in the data class itself, the below exception will never be called).
            raise Exception(f"A systemIntent as already been created. Make sure that you do not tried to show"
                            f"another interactive (or static element) that use a systemIntent somewhere else.")

        self.payload.google.systemIntent.data.listSelect.add_item(
            identifier_key=identifier_key, title=item_title, description=item_description,
            image_url=item_image_url, image_accessibility_text=item_image_accessibility_text
        )

    def add_interactive_carousel_item_to_system_intent(
            self, identifier_key: str, item_title: str, item_description: str,
            item_image_url: str = None, item_image_accessibility_text: str = None
    ) -> bool:
        """
        :return bool: True if the SystemIntent has been created and so we just set
        the first interactive element in the invocation and False otherwise
        """
        is_first_interactive_element_of_invocation = False
        if "systemIntent" not in vars(self.payload.google):
            self.payload.google.systemIntent = SystemIntent(element_type=SystemIntent._ELEMENT_TYPE_CAROUSEL_SELECT)
            is_first_interactive_element_of_invocation = True
        elif self.payload.google.systemIntent.data.carouselSelect is None:
            # If the carouselSelect variable is None, it means that the SystemIntent do not represent a carouselSelect,
            # and an exception will be thrown (in the data class itself, the below exception will never be called).
            raise Exception(f"A systemIntent as already been created. Make sure that you do not tried to show"
                            f"another interactive (or static element) that use a systemIntent somewhere else.")

        self.payload.google.systemIntent.data.carouselSelect.add_item(
            identifier_key=identifier_key, title=item_title, description=item_description,
            image_url=item_image_url, image_accessibility_text=item_image_accessibility_text
        )
        return is_first_interactive_element_of_invocation

    def add_item_to_audio_media_response(
            self, mp3_file_url: str, name: str, description: str = None,
            icon_image_url: str = None, icon_accessibility_text: str = None
    ) -> None:
        media_response_instance = None
        # todo: improve this loop so that we do not need to loop every time we add an item
        for response_item in self.payload.google.richResponse.items:
            if isinstance(response_item, MediaResponse):
                media_response_instance = response_item
                break
        if media_response_instance is None:
            media_response_instance = MediaResponse()
            self.payload.google.richResponse.items.append(media_response_instance)
        media_response_instance.add_audio_content(
            mp3_file_url=mp3_file_url, name=name, description=description,
            icon_image_url=icon_image_url, icon_accessibility_text=icon_accessibility_text
        )

    def request_push_notifications_permission(self, intent_name: str) -> None:
        self.payload.google.systemIntent = SystemIntent(
            element_type=SystemIntent._ELEMENT_TYPE_ASK_PERMISSION,
            permissions_update_intent_name=intent_name
        )

    def to_dict(self) -> dict:
        return self.dict()
