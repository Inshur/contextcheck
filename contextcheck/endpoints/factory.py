from contextcheck.endpoints.endpoint import EndpointBase, EndpointConfig
from contextcheck.endpoints.endpoint_cc_prompt_llm import EndpointCCPromptLLM
from contextcheck.endpoints.endpoint_openai import EndpointOpenAI
from contextcheck.endpoints.endpoint_tg_chatbot import EndpointTGChatBot

endpoint_map = {
    "openai": EndpointOpenAI,
    "cc_prompt_llm": EndpointCCPromptLLM,
    "tg_chatbot": EndpointTGChatBot,
}


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        endpoint_class = endpoint_map[kind]
    except KeyError:
        raise ValueError("No endpoint for this kind of config.")

    return endpoint_class(config=endpoint_config)


# def factory(endpoint_config: EndpointConfig) -> EndpointBase:
#     kind = endpoint_config.kind
#     try:
#         ep_cls = next(
#             cls for cls in EndpointBase.__subclasses__() if cls.kind == kind
#         )
#     except StopIteration:
#         raise ValueError("No endpoint for this kind of config.")
#     return ep_cls(config=endpoint_config)
