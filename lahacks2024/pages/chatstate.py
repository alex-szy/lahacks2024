import reflex as rx
import os
import asyncio
# from openai import AsyncOpenAI

class State(rx.State):
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    # chat_history: list[tuple[str, str]]
    
    # async def answer(self):
    #     # Our chatbot is not very smart right now...
    #     answer = "I don't know!"
    #     #answer = ""
    #     self.chat_history.append((self.question, ""))

    #     # Clear the question input.
    #     self.question = ""
    #     # Yield here to clear the frontend input before continuing.
    #     yield

    #     for i in range(len(answer)):
    #         # Pause to show the streaming effect.
    #         await asyncio.sleep(0.1)
    #         # Add one letter at a time to the output.
    #         self.chat_history[-1] = (
    #             self.chat_history[-1][0],
    #             answer[: i + 1],
    #         )
    #         yield
