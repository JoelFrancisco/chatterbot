from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.logic import SpecificResponseAdapter
from chatterbot import ChatBot
import json
import os

def add_response(question, response):
    with open('training.json', 'wr') as f:
        obj = json.load(f)
        obj[question] = response
        json.dump(x, f)
        f.write(x)

bot = ChatBot("Test 01",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Não entendi a pergunta meu patrão",
            "maximum_similarity_threshold": 0.60
        },
        {
            "import_path": 'chatterbot.logic.SpecificResponseAdapter',
            "input_text": 'teste',
            "output_text": 'resultado teste'
        }
    ]
)

list_trainer = ListTrainer(bot)

with open('training.json') as f:
    training = json.load(f)
    for x in training['conversations']:
        list_trainer.train(x)

corpus_trainer = ChatterBotCorpusTrainer(bot)

corpus_trainer.train("chatterbot.corpus.portuguese")

# conversation = ['oi', 'olá', 'bom dia', 'hello my little friend']

while True:
    try:
        question = input('Voce: ')

        response = bot.get_response(question)
        if response == 'Não entendi a pergunta meu patrão':
            answer = input('Deseja adicionar uma resposta? s/n ')
            if answer.lower() == 's':
                new_response = input('Qual seria a resposta: ')
                add_response(question, new_response)

        print('Bot:', response)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

