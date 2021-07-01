#Imports
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
import json

#Função que adiciona a resposta no arquivo de treino
def add_response(question, response):
    x = None
    with open('training.json') as fp: #Lê o arquivo e converte para um dicionário 
        x = json.loads(fp.read())

    x['conversations'].append([question, response]) #Adiciona resposta

    with open('training.json', 'w') as f: #Salva arquivo
        json.dump(x, f)  



bot = ChatBot("Test 01", #Cria uma instância do bot
    logic_adapters=[ #Adaptadores lógicos
        { #Adaptador de melhor reposta, esse está funcionando corretamente
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Não entendi a pergunta meu patrão",
            "maximum_similarity_threshold": 0.60
        },
        { #Adaptador de reposta específica, esse não está funcionando corretamente
            "import_path": 'chatterbot.logic.SpecificResponseAdapter',
            "input_text": 'teste',
            "output_text": 'resultado teste'
        }
    ]
)

list_trainer = ListTrainer(bot) #Instância objeto de treinamento com lista 

with open('training.json') as f: #Lê o arquivo para poder treinar o bot
    x = json.loads(f.read())
    for value in x['conversations']:
        list_trainer.train(value)

corpus_trainer = ChatterBotCorpusTrainer(bot) #Instância um objeto de treinos com dados que vem junto a lib

corpus_trainer.train("chatterbot.corpus.portuguese") #Treina o bot com os dados em português

while True:
    try:
        question = input('Voce: ') #Recebe input

        response = bot.get_response(question) #Consegue resposta do bot
        print('Bot:', response) #Print resposta do bot

        if str(response) == 'Não entendi a pergunta meu patrão': #Caso não tenha sido entendi 
            answer = input('Deseja adicionar uma resposta? s/n ') #Pergunta se deseja adicionar resposta
            if answer.lower() == 's': #Caso a resposta anterior seja sim, continua
                new_response = input('Qual seria a resposta: ') #Pergunta a resposta da pergunta
                add_response(question, new_response) #Chama a função para adicionar resposta no arquivo de treino

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
