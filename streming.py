import typing

from langchain_core.callbacks import BaseCallbackHandler


class StreamlitStreamingCallback(
    BaseCallbackHandler,
):
    def __init__(
            self,
            container: typing.Any,
    ):
        self.container = container
        self.accumulated_text = ""

    def on_llm_new_token(
            self,
            token: str,
            **kwargs,
    ) -> None:
        self.accumulated_text += token
        self.container.text(
            self.accumulated_text,
        )