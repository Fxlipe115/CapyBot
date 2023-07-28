import os
import openai
from slack_sdk.models.blocks import ImageBlock
from slack_sdk.models.blocks.basic_components import TextObject
from functions.callable_function import CallableFunction

from assistant.types import AssistantAnswer

class GenerateImage(CallableFunction):
    prompt: str

    def call(self) -> AssistantAnswer:
        print(f'Generating image with prompt: {self.prompt}')

        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.Image.create(
            prompt=self.prompt,
            n=1,
            size="512x512"
        )
        return AssistantAnswer(
            text='Here is your generated image:',
            blocks=[
                ImageBlock(
                    image_url=response['data'][0]['url'],
                    title=TextObject(
                        text=self.prompt
                    ),
                    alt_text=self.prompt
                )
            ]
        )
