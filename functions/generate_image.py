import os
import openai
from assistant.types import AssistantAnswer
from functions.callable_function import CallableFunction
from slack_message.types.blocks import ImageBlock


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
        return {
            'text': 'Here is your generated image:',
            'blocks': [
                {
                    'type': 'image',
                    'image_url': response['data'][0]['url'],
                    'title': {
                        'type': 'plain_text',
                        'text': self.prompt
                    },
                    'alt_text': self.prompt
                }
            ]
        }
