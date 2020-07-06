# from inoft_vocal_engine.platforms_handlers.handler_input import HandlerInput

KEY_INTERACTIONS_HISTORY = "interactions_history"
KEY_PLAYED_CATEGORIES_TYPES_HISTORY = "played_categories_types_history"
TYPE_NAME_NO_CATEGORY_TYPE_PLAYED_IN_CURRENT_SESSION = "NO_CATEGORY_TYPE_PLAYED_IN_CURRENT_SESSION"
HandlerInput = None

def get_session_attr(handler_input: HandlerInput):
    session_attr = handler_input.attributes_manager.session_attributes
    if not isinstance(session_attr, dict):
        handler_input.attributes_manager.session_attributes = dict()
        session_attr = handler_input.attributes_manager.session_attributes
    return session_attr

def set_session_attribute_element(handler_input: HandlerInput, element_key, element_values):
    get_session_attr(handler_input)[element_key] = element_values

def add_new_interaction(handler_input: HandlerInput, new_interaction_name: str):
    session_attr = get_session_attr(handler_input=handler_input)
    if KEY_INTERACTIONS_HISTORY not in session_attr.keys():
        session_attr[KEY_INTERACTIONS_HISTORY] = list()

    if len(session_attr[KEY_INTERACTIONS_HISTORY]) > 1:
        session_attr[KEY_INTERACTIONS_HISTORY].reverse()
    session_attr[KEY_INTERACTIONS_HISTORY].append(new_interaction_name)
    if len(session_attr[KEY_INTERACTIONS_HISTORY]) > 1:
        session_attr[KEY_INTERACTIONS_HISTORY].reverse()

def get_interactions_history(handler_input: HandlerInput):
    return get_session_attr(handler_input)[KEY_INTERACTIONS_HISTORY]

def add_new_played_category(handler_input: HandlerInput, new_played_interactions_types):
    session_attr = get_session_attr(handler_input=handler_input)
    if KEY_PLAYED_CATEGORIES_TYPES_HISTORY not in session_attr.keys():
        session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY] = list()

    if len(session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY]) > 1:
        session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY].reverse()
    session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY].append(new_played_interactions_types)
    if len(session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY]) > 1:
        session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY].reverse()

def get_played_categories_types_history(handler_input: HandlerInput):
    session_attr = get_session_attr(handler_input)
    if KEY_PLAYED_CATEGORIES_TYPES_HISTORY not in session_attr.keys():
        return list(TYPE_NAME_NO_CATEGORY_TYPE_PLAYED_IN_CURRENT_SESSION)
    return get_session_attr(handler_input)[KEY_PLAYED_CATEGORIES_TYPES_HISTORY]

class PlayedCategoriesTypesHistory:
    def __init__(self, handler_input: HandlerInput):
        session_attr = get_session_attr(handler_input)
        if KEY_PLAYED_CATEGORIES_TYPES_HISTORY not in session_attr.keys():
            session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY] = list()
        self.categories_types_history_values = session_attr[KEY_PLAYED_CATEGORIES_TYPES_HISTORY]
        print(f"Played categories types history values = {self.categories_types_history_values}")

    def get_last(self):
        if (self.categories_types_history_values is None
        or not len(self.categories_types_history_values) > 0
        or self.categories_types_history_values[0] is None):
            return list()
        else:
            return self.categories_types_history_values[0]

def get_skill_application_id(handler_input: HandlerInput) -> str:
    return handler_input.request_envelope.context.system.application.application_id
