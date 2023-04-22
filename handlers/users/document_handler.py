from llama_index import SimpleDirectoryReader, download_loader
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper, ServiceContext
from langchain import OpenAI

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import Command, Message
from states.bot_states import UploadWaiterState, AskQuestion

from loader import dp
from loader import bot


@dp.message_handler(Command('insert'))
async def insert(message: types.Message):
    await message.answer(f"Please Insert a document, {message.from_user.full_name}!")
    await UploadWaiterState.Upload.set()
 

# Define your handler function to handle user-uploaded documents
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=UploadWaiterState.Upload)
async def handle_document(message: Message, state: FSMContext):
    if message.document:
        # Use the bot's getFile method to retrieve the file
        file = await bot.get_file(message.document.file_id)

        # Save the file in the ./data folder
        file_path = f"./data/user_docs/{message.document.file_name}"
        await file.download(destination=file_path)
        # Send a success message back to the user
        await message.reply(f"File saved as {file_path}")
        await state.finish()

    else:
        # If the user uploads a file that is not a document, send an error message
        await message.reply("Please upload a document.")



def read_doc():
    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader('./data/user_docs', recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    return documents


def construct_index(document):
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    
    index = GPTSimpleVectorIndex.from_documents(
        document, service_context=service_context
    )

    index.save_to_disk('index.json')

@dp.message_handler(commands="train")
async def train_model(message: Message):
    
        await message.answer("Reading the document")
        document = read_doc()
        construct_index(document)
        await message.answer("Successfully learned the document. Now you can Ask anything.")
        await AskQuestion.Ask.set()


@dp.message_handler(state=AskQuestion.Ask)
async def ask_questions(message: Message, state:FSMContext):

    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(message.text, response_mode="tree-summarize")
    await message.reply((response))