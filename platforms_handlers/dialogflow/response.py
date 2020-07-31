from json import dumps as json_dumps
from typing import Optional

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict

# todo: add select carousel
# todo: add select list

class OpenUrlAction:
    json_key = "openUrlAction"

    def __init__(self, url: str):
        self.url = url

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        if not isinstance(url, str):
            raise Exception(f"url was type {type(url)} which is not valid value for his parameter.")
        self._url = url

class Image:
    json_key = "image"

    def __init__(self, image_url: str, accessibility_text: str = None):
        self.url = image_url
        if accessibility_text is not None:
            # The accessibility_text is not required
            self.accessibilityText = accessibility_text
        else:
            self._accessibilityText = None

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        if not isinstance(url, str):
            raise Exception(f"url was type {type(url)} which is not valid value for his parameter.")
        self._url = url

    @property
    def accessibilityText(self) -> str:
        return self._accessibilityText

    @accessibilityText.setter
    def accessibilityText(self, accessibilityText: str) -> None:
        if accessibilityText is not None and not isinstance(accessibilityText, str):
            raise Exception(f"accessibilityText was type {type(accessibilityText)} which is not valid value for his parameter.")
        self._accessibilityText = accessibilityText


class Icon(Image):
    json_key = "icon"
    # todo: make sure that when a class inherite from another, we use the icon json_key and not the image key

    def __init__(self, image_url: str, accessibility_text: str = None):
        super().__init__(image_url=image_url, accessibility_text=accessibility_text)

class ImageDisplayOptions:
    json_key = "imageDisplayOptions"

    cropped_type = "CROPPED"
    available_options_types = [cropped_type]

    def __init__(self, option_type: str):
        self.option_type = option_type

    @property
    def option_type(self) -> str:
        return self._option_type

    @option_type.setter
    def option_type(self, option_type: str) -> None:
        if not isinstance(option_type, str):
            raise Exception(f"option_type was type {type(option_type)} which is not valid value for his parameter.")
        if option_type not in self.available_options_types:
            raise Exception(f"The option_type {option_type} was not a valid display options type.")
        self._option_type = option_type

class Button:
    json_key = "button"

    def __init__(self):
        self._title = str()
        self._openUrlAction = str()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        if not isinstance(title, str):
            raise Exception(f"title was type {type(title)} which is not valid value for his parameter.")
        self._title = title

    @property
    def openUrlAction(self) -> str:
        return self._openUrlAction

    @openUrlAction.setter
    def openUrlAction(self, openUrlAction: str) -> None:
        if not isinstance(openUrlAction, str):
            raise Exception(f"openUrlAction was type {type(openUrlAction)} which is not valid value for his parameter.")
        self._openUrlAction = openUrlAction

class BasicCard:
    json_key = "basicCard"

    def __init__(self, title: str, subtitle: str, formatted_text: str = None, buttons: list = None,
                 image: Image = None, image_display_options: ImageDisplayOptions = None):

        self._title = title
        self._subtitle = subtitle
        self._formattedText = formatted_text
        self._buttons = buttons
        self._image = image
        self._imageDisplayOptions = image_display_options

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        if not isinstance(title, str):
            raise Exception(f"title was type {type(title)} which is not valid value for his parameter.")
        self._title = title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str) -> None:
        if not isinstance(subtitle, str):
            raise Exception(f"subtitle was type {type(subtitle)} which is not valid value for his parameter.")
        self._subtitle = subtitle

    @property
    def formattedText(self) -> str:
        return self._formattedText

    @formattedText.setter
    def formattedText(self, formattedText: str) -> None:
        if not isinstance(formattedText, str):
            raise Exception(f"formattedText was type {type(formattedText)} which is not valid value for his parameter.")
        self._formattedText = formattedText

    @property
    def buttons(self) -> list:
        return self._buttons

    @buttons.setter
    def buttons(self, buttons: list) -> None:
        if not isinstance(buttons, list):
            raise Exception(f"buttons was type {type(buttons)} which is not valid value for his parameter.")
        self._buttons = buttons

    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image: Image) -> None:
        if not isinstance(image, Image):
            raise Exception(f"image was type {type(image)} which is not valid value for his parameter.")
        self._image = image

    @property
    def imageDisplayOptions(self):
        return self._imageDisplayOptions

    @imageDisplayOptions.setter
    def imageDisplayOptions(self, imageDisplayOptionType: str) -> None:
        if not isinstance(imageDisplayOptionType, str):
            raise Exception(f"imageDisplayOptionType was type {type(imageDisplayOptionType)} which is not valid value for his parameter.")
        self._imageDisplayOptions.option_type = imageDisplayOptionType

    def return_transformations(self) -> None:
        self._imageDisplayOptions = self._imageDisplayOptions if self._imageDisplayOptions is None else self._imageDisplayOptions.option_type()


# todo: check if an image/video url is valid and throw an exception if not
# todo: raise for google if more than 2 response items have been set
# todo: do not allow to use elements that the plateform cannot support (like a carousel need to be on a platform that support a web browser, like a phone)

class BrowseCarousel:
    json_key = "carouselBrowse"

    def __init__(self):
        self._items = list()
        self._first_item_used_keys = None

    @property
    def items(self) -> list:
        return self._items

    def add_item(self, title: str, url_to_open_on_click: str, description: str = None,
                 image_url: str = None, image_accessibility_text: str = None, footer: str = None):

        if len(self._items) < 10:
            # A carousel can have a maximum of 10 items
            item = self.Item(title=title, description=description, openUrlAction=OpenUrlAction(url=url_to_open_on_click), footer=footer,
                             image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text))

            if self._first_item_used_keys is None:
                self._first_item_used_keys = ["title", "url_to_open_on_click"]
                if description is not None:
                    self._first_item_used_keys.append("description")
                if image_url is not None:
                    self._first_item_used_keys.append("image_url")
                if image_accessibility_text is not None:
                    self._first_item_used_keys.append("image_accessibility_text")
                if footer is not None:
                    self._first_item_used_keys.append("footer")
            else:
                if (("description" in self._first_item_used_keys if description is None else "description" not in self._first_item_used_keys)
                or ("image_url" in self._first_item_used_keys if image_url is None else "image_url" not in self._first_item_used_keys)
                or ("image_accessibility_text" in self._first_item_used_keys if image_accessibility_text is None else "image_accessibility_text" not in self._first_item_used_keys)
                or ("footer" in self._first_item_used_keys if footer is None else "footer" not in self._first_item_used_keys)):
                    raise Exception(f"All carousel items must have the same variable, to assure a tile consistency."
                                    f"The first item of the carousel had the following variables : {self._first_item_used_keys}"
                                    f"which are not the same as the last item you inserted : {item.__dict__}")

            self._items.append(item)
        else:
            print("The browse carousel items limit of 10 has ben reached. Your new item has not been included.")

    def do_not_include(self):
        # If no items are present in the carousel, we do not include it
        if len(self._items) == 0:
            return True
        else:
            return False

    def return_transformations(self) -> None:
        if self.do_not_include() is False and len(self._items) == 1:
            # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
            first_item = self._items[0]
            if isinstance(first_item, self.Item):
                self._items.append(self.Item(title=first_item.title, description=first_item.description, image=first_item.image,
                                             openUrlAction=first_item.openUrlAction, footer=first_item.footer))
                print(f"Warning, a carousel had only one item, since we require two items, the only one has been duplicated.")
            else:
                raise Exception(f"The first_item of the carousel was not an instance of carousel item but {first_item}")

        del self._first_item_used_keys
        # The first_item_used_keys variable is only for backend practices and should not be
        # included in the response, so we delete the attributes on the return transformations.

    class Item:
        json_key = None

        def __init__(self, title: str, description: str = None, image: Image = None, openUrlAction: OpenUrlAction = None, footer: str = None):
            self.title = title
            self.description = description
            self.image = image
            self.openUrlAction = openUrlAction
            self.footer = footer

        @property
        def title(self) -> str:
            return self._title

        @title.setter
        def title(self, title: str) -> None:
            if not isinstance(title, str):
                raise Exception(f"title was type {type(title)} which is not valid value for his parameter.")
            self._title = title

        @property
        def description(self) -> str:
            return self._description

        @description.setter
        def description(self, description: str) -> None:
            if description is not None and not isinstance(description, str):
                raise Exception(f"description was type {type(description)} which is not valid value for his parameter.")
            self._description = description

        @property
        def image(self):
            return self._image

        @image.setter
        def image(self, image: Image) -> None:
            if image is not None and not isinstance(image, Image):
                raise Exception(f"image was type {type(image)} which is not valid value for his parameter.")
            self._image = image

        @property
        def openUrlAction(self):
            return self._openUrlAction

        @openUrlAction.setter
        def openUrlAction(self, openUrlAction: OpenUrlAction) -> None:
            if openUrlAction is not None and not isinstance(openUrlAction, OpenUrlAction):
                raise Exception(f"openUrlAction was type {type(openUrlAction)} which is not valid value for his parameter.")
            self._openUrlAction = openUrlAction

        @property
        def footer(self):
            return self._footer

        @footer.setter
        def footer(self, footer: str) -> None:
            if footer is not None and not isinstance(footer, str):
                raise Exception(f"footer was type {type(footer)} which is not valid value for his parameter.")
            self._footer = footer


class MediaResponse:
    json_key = "mediaResponse"
    key_media_type_audio = "AUDIO"
    available_media_types_keys = [key_media_type_audio]

    # todo: check that the user device has the capability to play audio files in a media response
    # todo: add follow up when audio file has finished playing

    def __init__(self):
        self._mediaType = None
        self._mediaObjects = list()

    @property
    def mediaType(self) -> str:
        return self._mediaType

    @mediaType.setter
    def mediaType(self, mediaType: str) -> None:
        if mediaType not in self.available_media_types_keys:
            raise Exception(f"The media_type {mediaType} was not found in the available media types list : {self.available_media_types_keys}")
        self._mediaType = mediaType

    @property
    def mediaObjects(self) -> list:
        return self._mediaObjects

    def add_audio_content(self, mp3_file_url: str, name: str, description: str = None,
                          icon_image_url: str = None, icon_accessibility_text: str = None):
        # todo: check validity of mp3 file, otherwise print a warning and do not add the item
        #  (and if it was the only item, do not include the media response)

        if self.mediaType is None:
            self.mediaType = self.key_media_type_audio
        else:
            if self.mediaType != self.key_media_type_audio:
                raise Exception(f"You cannot add an audio content object if you have already instantiated a media"
                                f"object by adding a different content that is of media type {self.mediaType}")

        self.mediaObjects.append(self.MediaObject(content_url=mp3_file_url, name=name, description=description,
                                                  icon=None if icon_image_url is None else Icon(image_url=icon_image_url,
                                                                                                accessibility_text=icon_accessibility_text)))

    class MediaObject:
        json_key = None

        def __init__(self, content_url: str, name: str, description: str = None, icon: Icon = None):
            self.contentUrl = content_url
            self.name = name
            self.description = description
            self.icon = icon

        @property
        def contentUrl(self) -> str:
            return self._contentUrl

        @contentUrl.setter
        def contentUrl(self, contentUrl: str) -> None:
            if contentUrl is not None and not isinstance(contentUrl, str):
                raise Exception(f"contentUrl was type {type(contentUrl)} which is not valid value for his parameter.")
            self._contentUrl = contentUrl

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, name: str) -> None:
            if name is not None and not isinstance(name, str):
                raise Exception(f"name was type {type(name)} which is not valid value for his parameter.")
            self._name = name

        @property
        def description(self):
            return self._description

        @description.setter
        def description(self, description: str) -> None:
            if description is not None and not isinstance(description, str):
                raise Exception(f"description was type {type(description)} which is not valid value for his parameter.")
            self._description = description

        @property
        def icon(self):
            return self._icon

        @icon.setter
        def icon(self, icon: Icon) -> None:
            if icon is not None and not isinstance(icon, Icon):
                raise Exception(f"icon was type {type(icon)} which is not valid value for his parameter.")
            self._icon = icon


class SystemIntent:
    json_key = "systemIntent"
    intent_type_option = "actions.intent.OPTION"
    intent_type_permission = "actions.intent.PERMISSION"
    available_intent_keys_types = [intent_type_option, intent_type_permission]
    element_type_list_select = "ListSelect"
    element_type_carousel_select = "CarouselSelect"
    element_type_ask_permission = "AskPermission"
    option_elements_types_keys = [element_type_list_select, element_type_carousel_select]
    permission_elements_types_keys = [element_type_ask_permission]

    def __init__(self, element_type: str, permissions_update_intent_name: Optional[str] = None):
        if element_type in self.option_elements_types_keys:
            self.intent = self.intent_type_option
        elif element_type in self.permission_elements_types_keys:
            self.intent = self.intent_type_permission
        else:
            raise Exception(f"The element_type '{element_type}' for the SystemIntent as not been recognized.")

        self._data = self.Data(element_type=element_type, permissions_update_intent_name=permissions_update_intent_name)

    @property
    def intent(self) -> str:
        return self._intent

    @intent.setter
    def intent(self, intent_type: str) -> None:
        if intent_type not in self.available_intent_keys_types:
            raise Exception(f"The key_type {intent_type} was not found in the intent keys types list : {self.available_intent_keys_types}")
        self._intent = intent_type

    class Data:
        json_key = "data"

        def __init__(self, element_type: str, permissions_update_intent_name: Optional[str] = None):
            if element_type == SystemIntent.element_type_list_select:
                self._type = "type.googleapis.com/google.actions.v2.OptionValueSpec"
                self._listSelect = self.ListSelect()
            elif element_type == SystemIntent.element_type_carousel_select:
                self._type = "type.googleapis.com/google.actions.v2.OptionValueSpec"
                self._carouselSelect = self.CarouselSelect()
            elif element_type == SystemIntent.element_type_ask_permission:
                if permissions_update_intent_name is None:
                    raise Exception(f"The intent_name argument in the request_push_notifications_permission_if_missing function has not been defined.")
                self._type = "type.googleapis.com/google.actions.v2.PermissionValueSpec"
                self._permissions = ["UPDATE"]
                self._updatePermissionValueSpec = self.UpdatePermissionValueSpec(intent=permissions_update_intent_name)
            else:
                raise Exception(f"The element_type {element_type} is not a supported element type.")

        @property
        def type(self) -> str:
            return self._type

        @type.setter
        def type(self, type_key: str) -> None:
            if not isinstance(type_key, str):
                raise Exception(f"type was type {type(type_key)} which is not valid value for his parameter.")
            self._type = type_key

        def return_transformations(self):
            # The key that google is expecting is the @type key, yet since in python i cannot directly set a variable
            # with the @type name, we use a simple '_type' variable name, and in the return transformations, we create
            # a new var called '@type' with the vars dict to which we assign the value of the 'type' property (it points
            # to the '_type' variable) and then we can delete the '_type' variable to not include it in the output dict.
            vars(self)["@type"] = self.type
            del self._type

        class InteractiveListOrCarouselItem:
            json_key = None

            def __init__(self, identifier_key: str, title: str, description: str = None, image: Image = None):
                self._title = title
                self._description = description
                self._image = image
                self._optionInfo = self.OptionInfo(identifier_key=identifier_key)

            @property
            def title(self) -> str:
                return self._title

            @title.setter
            def title(self, title: str) -> None:
                raise_if_variable_not_expected_type(value=title, expected_type=str, variable_name="title")
                self._title = title

            @property
            def description(self) -> str:
                return self._description

            @description.setter
            def description(self, description: str) -> None:
                raise_if_variable_not_expected_type(value=description, expected_type=str, variable_name="description")
                self._description = description

            @property
            def image(self) -> Image:
                return self._image

            @image.setter
            def image(self, image: Image) -> None:
                raise_if_variable_not_expected_type(value=image, expected_type=Image, variable_name="image")
                self._image = image

            class OptionInfo:
                json_key = "optionInfo"

                def __init__(self, identifier_key: str):
                    self.key = identifier_key
                    import random  # todo: check if synonyms are required and add possibility to set them
                    self._synonyms = [f"{random.randint(0, 1000000000000000)}"]

                @property
                def key(self) -> str:
                    return self._key

                @key.setter
                def key(self, key: str) -> None:
                    raise_if_variable_not_expected_type(value=key, expected_type=str, variable_name="key")
                    self._key = key

                @property
                def synonyms(self) -> list:
                    return self._synonyms

                @synonyms.setter
                def synonyms(self, synonyms_list: list) -> None:
                    raise_if_variable_not_expected_type(value=synonyms_list, expected_type=list, variable_name="synonyms_list")
                    self._synonyms = synonyms_list

            @property
            def optionInfo(self) -> OptionInfo:
                return self._optionInfo

        class ListSelect:
            json_key = "listSelect"

            def __init__(self):
                self._title = str()
                self._items = list()

            def add_item(self, identifier_key: str, title: str, description: str = None,
                         image_url: str = None, image_accessibility_text: str = None):

                if len(self._items) < 30:
                    self.items.append(SystemIntent.Data.InteractiveListOrCarouselItem(
                        identifier_key=identifier_key, title=title, description=description,
                        image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text)))
                else:
                    print("The list items limit of 30 has ben reached. Your new item has not been included.")

            def do_not_include(self):
                # If no items are present in the list, we do not include it
                if len(self.items) == 0:
                    return True
                else:
                    return False

            def return_transformations(self) -> None:
                if self.do_not_include() is False and len(self._items) == 1:
                    # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
                    first_item = self.items[0]
                    if isinstance(first_item, SystemIntent.Data.InteractiveListOrCarouselItem):
                        new_identifier_key = f"{first_item.optionInfo.key}.2"
                        self.items.append(SystemIntent.Data.InteractiveListOrCarouselItem(
                            identifier_key=new_identifier_key, title=f"2 - {first_item.title}",
                            description=first_item.description, image=first_item.image))

                        first_item.title = f"1 - {first_item.title}"
                        print(f"Warning, a list had only one item, since we require two items, the only one has been duplicated"
                              f"with a new id of {new_identifier_key} instead of dumbly duplicating the id {first_item.optionInfo.key}"
                              f"A '1 -' and a '2 -' have also been added to the elements titles, to make them both uniques.")
                    else:
                        raise Exception(f"The first_item of the list was not an instance of list item but {first_item}")

            @property
            def title(self) -> str:
                return self._title

            @title.setter
            def title(self, title: str) -> None:
                raise_if_variable_not_expected_type(value=title, expected_type=str, variable_name="title")
                self._title = title

            @property
            def items(self) -> list:
                return self._items

            @items.setter
            def items(self, items_list: list) -> None:
                raise_if_variable_not_expected_type(value=items_list, expected_type=list, variable_name="items_list")
                self._items = items_list

        @property
        def listSelect(self) -> ListSelect:
            if "_listSelect" not in vars(self):
                raise Exception(f"The SystemIntent was not set to a ListSelect. Did you tried to show different types"
                                f"of elements that run with a SystemIntent, in the same execution of your app ?")
            else:
                return self._listSelect

        class CarouselSelect:
            json_key = "carouselSelect"

            def __init__(self):
                self._items = list()

            def add_item(self, identifier_key: str, title: str, description: str,
                         image_url: str = None, image_accessibility_text: str = None):

                if len(self._items) < 10:
                    self.items.append(SystemIntent.Data.InteractiveListOrCarouselItem(
                        identifier_key=identifier_key, title=title, description=description,
                        image=None if image_url is None else Image(image_url=image_url, accessibility_text=image_accessibility_text)))
                else:
                    print("The carousel items limit of 10 has ben reached. Your new item has not been included.")

            def do_not_include(self):
                # If no items are present in the carousel, we do not include it
                if len(self.items) == 0:
                    return True
                else:
                    return False

            def return_transformations(self) -> None:
                if self.do_not_include() is False and len(self._items) == 1:
                    # If the carousel has only one item, we duplicate it, because a carousel need at least 2 items
                    first_item = self.items[0]
                    if isinstance(first_item, SystemIntent.Data.InteractiveListOrCarouselItem):
                        new_identifier_key = f"{first_item.optionInfo.key}.2"
                        self.items.append(SystemIntent.Data.InteractiveListOrCarouselItem(
                            identifier_key=new_identifier_key, title=f"2 - {first_item.title}",
                            description=first_item.description, image=first_item.image))

                        first_item.title = f"1 - {first_item.title}"
                        print(f"Warning, a list had only one item, since we require two items, the only one has been duplicated"
                              f"with a new id of {new_identifier_key} instead of dumbly duplicating the id {first_item.optionInfo.key}"
                              f"A '1 -' and a '2 -' have also been added to the elements titles, to make them both uniques.")
                    else:
                        raise Exception(f"The first_item of the list was not an instance of list item but {first_item}")

            @property
            def items(self) -> list:
                return self._items

            @items.setter
            def items(self, items_list: list) -> None:
                raise_if_variable_not_expected_type(value=items_list, expected_type=list, variable_name="items_list")
                self._items = items_list

        @property
        def carouselSelect(self) -> CarouselSelect:
            if "_carouselSelect" not in vars(self):
                raise Exception(f"The SystemIntent was not set to a CarouselSelect. Did you tried to show different types"
                                f"of elements that run with a SystemIntent, in the same execution of your app ?")
            else:
                return self._carouselSelect

        @property
        def permissions(self) -> list:
            if "_permissions" not in vars(self):
                raise Exception(f"The SystemIntent did not have a permissions variable. Did you tried to show different types"
                                f"of elements that run with a SystemIntent, in the same execution of your app ?")
            else:
                return self._permissions

        class UpdatePermissionValueSpec:
            json_key = "updatePermissionValueSpec"

            def __init__(self, intent: str):
                self._intent = intent

            @property
            def intent(self) -> str:
                return self._intent



        @property
        def updatePermissionValueSpec(self) -> UpdatePermissionValueSpec:
            if "_updatePermissionValueSpec" not in vars(self):
                raise Exception(f"The SystemIntent did not have a updatePermissionValueSpec variable. Did you tried to show "
                                f"different types of elements that run with a SystemIntent, in the same execution of your app ?")
            else:
                return self._updatePermissionValueSpec

    @property
    def data(self) -> Data:
        return self._data

class SimpleResponse:
    json_key = "simpleResponse"

    def __init__(self):
        self._textToSpeech = str()
        self._displayText = str()

    @property
    def textToSpeech(self):
        return self._textToSpeech

    @textToSpeech.setter
    def textToSpeech(self, text: str) -> None:
        if isinstance(text, str):
            self._textToSpeech = text
        else:
            raise Exception(f"The text was not a string object : {text}")

    @property
    def displayText(self):
        return self._textToSpeech

    @displayText.setter
    def displayText(self, text: str) -> None:
        if isinstance(text, str):
            self._displayText = text
        else:
            raise Exception(f"The text was not a string object : {text}")


class RichResponseInPayload:
    json_key = "richResponse"

    def __init__(self):
        self._items = list()
        self.suggestions = list()

    @property
    def items(self):
        return self._items

    def add_response_item(self, response_item_object) -> int:
        """:return Length of the list containing all the response items"""
        self._items.append(response_item_object)
        return len(self._items) - 1

    def add_suggestion_chip(self, title: str):
        # todo: add external link suggestion chip (cannot be used on platforms without the actions.capability.WEB_BROWSER capability
        if not isinstance(title, str):
            raise Exception(f"The title variable must be of type str but was {type(title)}")
        if len(title) > 25:
            raise Exception(f"A suggestion chip title can have a maximum of 25 chars but {title} was {len(title)} chars")

        self.suggestions.append({"title": title})

    def return_transformations(self):
        for i in range(len(self.items)):
            self.items[i] = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self.items[i],
                                                                           key_names_identifier_objects_to_go_into=["json_key"])


class GoogleInPayload:
    json_key = "google"

    def __init__(self):
        self._expectUserResponse = True
        self.richResponse = RichResponseInPayload()
        self._userStorage = str()

    @property
    def expectUserResponse(self):
        return self._expectUserResponse

    @expectUserResponse.setter
    def expectUserResponse(self, expectUserResponse) -> None:
        raise_if_variable_not_expected_type(value=expectUserResponse, expected_type=bool, variable_name="expectUserResponse")
        self._expectUserResponse = expectUserResponse

    @property
    def userStorage(self) -> str:
        return self._userStorage

    @userStorage.setter
    def userStorage(self, userStorage: str) -> None:
        raise_if_variable_not_expected_type(value=userStorage, expected_type=str, variable_name="userStorage")
        self._userStorage = userStorage

class Payload:
    json_key = "payload"

    def __init__(self):
        self.google = GoogleInPayload()

    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])

class OutputContextItem:
    json_key = None
    session_data_name = "sessionData"

    def __init__(self, session_id: str, name: str, lifespanCount=999):
        self.name = f"{session_id}/contexts/{name}"
        self.lifespanCount = lifespanCount
        self._parameters = dict()

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
            self._parameters[parameter_key] = parameter_value
        return self

    def add_set_session_attribute(self, parameter_key: str, parameter_value=None):
        if "data" not in self.parameters.keys():
            self.parameters["data"] = dict()

        if parameter_value is not None and isinstance(parameter_key, str) and parameter_key != "":
            self._parameters["data"][parameter_key] = parameter_value
        return self

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: dict) -> None:
        if not isinstance(parameters, dict):
            raise Exception(f"parameters was type {type(parameters)} which is not valid value for his parameter.")
        self._parameters = parameters

class Response:
    json_key = "response"

    def __init__(self):
        self.payload = Payload()
        self.outputContexts = list()
        self._first_say_rich_response_list_id = None
        self._second_say_rich_response_list_id = None

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

    def end_session(self, should_end: bool = True):
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

    def add_item_to_browse_carousel(self, title: str,  url_to_open_on_click: str, description: str = None,
                                    image_url: str = None, image_accessibility_text: str = None, footer: str = None):

        carousel_instance = None
        # todo: improve this loop so that we do not need to loop every time we add an item
        for response_item in self.payload.google.richResponse.items:
            if isinstance(response_item, BrowseCarousel):
                carousel_instance = response_item
                break
        if carousel_instance is None:
            carousel_instance = BrowseCarousel()
            self.payload.google.richResponse.items.append(carousel_instance)
        carousel_instance.add_item(title=title, url_to_open_on_click=url_to_open_on_click, description=description,
                                   image_url=image_url, image_accessibility_text=image_accessibility_text, footer=footer)

    def add_interactive_list_item_to_system_intent(self, identifier_key: str, item_title: str, item_description: str = None,
                                                   item_image_url: str = None, item_image_accessibility_text: str = None) -> bool:

        if "systemIntent" not in vars(self.payload.google):
            self.payload.google.systemIntent = SystemIntent(element_type=SystemIntent.element_type_list_select)
        elif self.payload.google.systemIntent.data.listSelect is None:
            # If the listSelect variable is None, it means that the SystemIntent do not represent a ListSelect,
            # and an exception will be thrown (in the data class itself, the below exception will never be called).
            raise Exception(f"A systemIntent as already been created. Make sure that you do not tried to show"
                            f"another interactive (or static element) that use a systemIntent somewhere else.")

        self.payload.google.systemIntent.data.listSelect.add_item(identifier_key=identifier_key, title=item_title, description=item_description,
                                                                  image_url=item_image_url, image_accessibility_text=item_image_accessibility_text)

    def add_interactive_carousel_item_to_system_intent(self, identifier_key: str, item_title: str, item_description: str,
                                                       item_image_url: str = None, item_image_accessibility_text: str = None) -> bool:
        """
        :return bool: True if the SystemIntent has been created and so we just set the first interactive element in the invocation and False otherwise
        """

        is_first_interactive_element_of_invocation = False
        if "systemIntent" not in vars(self.payload.google):
            self.payload.google.systemIntent = SystemIntent(element_type=SystemIntent.element_type_carousel_select)
            is_first_interactive_element_of_invocation = True
        elif self.payload.google.systemIntent.data.carouselSelect is None:
            # If the carouselSelect variable is None, it means that the SystemIntent do not represent a carouselSelect,
            # and an exception will be thrown (in the data class itself, the below exception will never be called).
            raise Exception(f"A systemIntent as already been created. Make sure that you do not tried to show"
                            f"another interactive (or static element) that use a systemIntent somewhere else.")

        self.payload.google.systemIntent.data.carouselSelect.add_item(identifier_key=identifier_key, title=item_title, description=item_description,
                                                                      image_url=item_image_url, image_accessibility_text=item_image_accessibility_text)
        return is_first_interactive_element_of_invocation

    def add_item_to_audio_media_response(self, mp3_file_url: str, name: str, description: str = None,
                                         icon_image_url: str = None, icon_accessibility_text: str = None):

        media_response_instance = None
        # todo: improve this loop so that we do not need to loop every time we add an item
        for response_item in self.payload.google.richResponse.items:
            if isinstance(response_item, MediaResponse):
                media_response_instance = response_item
                break
        if media_response_instance is None:
            media_response_instance = MediaResponse()
            self.payload.google.richResponse.items.append(media_response_instance)
        media_response_instance.add_audio_content(mp3_file_url=mp3_file_url, name=name, description=description,
                                                  icon_image_url=icon_image_url, icon_accessibility_text=icon_accessibility_text)

    def request_push_notifications_permission(self, intent_name: str) -> None:
        self.payload.google.systemIntent = SystemIntent(element_type=SystemIntent.element_type_ask_permission, permissions_update_intent_name=intent_name)


    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])[self.json_key]


if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Payload(), ["json_key"])