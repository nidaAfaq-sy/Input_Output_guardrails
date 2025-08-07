from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import(
    input_guardrail,
    output_guardrail, 
    RunContextWrapper, 
    TResponseInputItem, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    )

import chainlit as cl


load_dotenv() 
set_tracing_disabled(disabled=True
                     )  
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
     api_key = gemini_api_key,
     base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
     model = "gemini-2.0-flash",
     openai_client = client
)




class OutputPython(BaseModel):
        is_python_related : bool
        reasoning : str

#  Guardrails Agent
input_guardrails_agent = Agent(
    name = "Input_Guardrails_Checker",
    instructions="Check it the user's question related to python programming, if it is, return true,if it is not, return false",
    model = "gpt-4o-mini",
    output_type=OutputPython
) 
# Guardrail Logic

@input_guardrail
async def input_guardrails_func(
    ctx: RunContextWrapper[None], agent:Agent, input: str | list[TResponseInputItem]
)->GuardrailFunctionOutput:
    result = await Runner.run(
        input_guardrails_agent,input)
    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= not result.final_output.is_python_related
    )

class MessageOutput(BaseModel):
     response : str

class PythonOutput(BaseModel):
     is_python_related : bool
     reasoning : str

output_guardrails_agent = Agent(
    name="Output_Guardrails",
    instructions="Check it he output includes any python related response" ,
    output_type=PythonOutput,
    model="gpt-4o-mini"
)
@output_guardrail
async def output_python_guardrails(
    ctx: RunContextWrapper[None], agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    output_result = await Runner.run(output_guardrails_agent, output)
    return GuardrailFunctionOutput(
        output_info=output_result.final_output,
        tripwire_triggered=not output_result.final_output.is_python_related
    )


main_agent = Agent(
    name = "Python Expert Agent",
    instructions= "You are a python expert agent, you respond only python related questions",
    model = "gpt-4o-mini",
    input_guardrails= [input_guardrails_func],
    output_guardrails=[output_python_guardrails]

)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Iam ready to assist you").send()

@cl.on_message
async def main(message: cl.Message):
   try:
        result = await Runner.run(
             main_agent,
             input=message.content
        )
        await cl.Message(content=result.final_output).send()
   except InputGuardrailTripwireTriggered: 
        await cl.Message(content="Please ask a python related question").send()

   except OutputGuardrailTripwireTriggered:
        await cl.Message(content="Output guardrail reject your querry").send()




