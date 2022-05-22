# -*- coding: UTF-8 -*-
"""
IA para ser usada no app
"""
import random
import os
import speech_recognition as sr
import pyttsx3
import cv2
import requests

from dotenv import load_dotenv

load_dotenv()  # carregando arquivo de variaveis de ambiante que vamos usar na API de clima
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 250)  # Seta velocidade de fala
engine.setProperty('voice', b'brasil')  # Seta linguagem


classifier = cv2.CascadeClassifier(
    './assets/haarcascade_frontalface_default.xml')  # Carregando o classificador

img = cv2.imread('./assets/rosto.png')  # Abrindo uma imagem para ser analisada
# Abrindo uma imagem para ser analisada
img2 = cv2.imread('./assets/rostos.png')

imgGray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # Convertendo para cinza

# Aplica o classificador na imagem em cinza
detected_faces = classifier.detectMultiScale(imgGray)


def talk(text):
    """
    Função para ser chamada sempre que formos realizar o TTS 
    """
    engine.say(text)
    engine.runAndWait()


def take_command():
    """
    Função generica para receber um comando
    """
    command = ""  # iniciando a variável vazia
    with sr.Microphone() as source:
        try:
            print("Escutando")  # Print para saber quando o programa inicia
            # Ouvindo o que o usuário vai falar
            voice = listener.listen(source)
            # Usa a API do google para realizar o STT
            command = listener.recognize_google(voice, language='pt')
            command = command.lower()

        except:
            pass

    return command


jogos = ["truco", "uno", "eu nunca", "verdade ou desafio", "poker"]


def sugerirJogo(jogos):
    """
    Função para sugerir um jogo da tabela de jogos existentes
    """
    jogo = random.choice(jogos)
    print(jogo)
    talk("Um jogo que você pode tentar é: " + jogo)


def integrantes():
    """
    Função que retorna os nomes dos criadores do aplicativo
    """
    integrantes = open("integrantes.txt", "r", encoding="utf-8")
    for lines in integrantes:
        talk(lines)
    integrantes.close()


def newGame():
    """
    Função que cadastra um novo jogo na base de dados do aplicativo
    """
    talk("Qual o nome do jogo?")
    bancoDeJogos = open("bancoDeJogos.txt", "a+", encoding="utf-8")
    name = take_command()
    bancoDeJogos.write("Jogo: " + name)
    bancoDeJogos.write("\n")
    talk("O que é preciso para jogar?")
    items = take_command()
    bancoDeJogos.write("Items: " + items)
    bancoDeJogos.write("\n")
    talk("Ok, jogo cadastrado")
    bancoDeJogos.close()


def ratingGame():
    """
    Função que permite o usuário avalizar os jogos já existentes
    """
    talk("Qual jogo quer avaliar?")
    bancoDeJogos = open("bancoDeJogos.txt", "a+", encoding="utf-8")
    game = take_command()
    print(game)
    bancoDeJogos.write("Jogo: " + game)
    bancoDeJogos.write("\n")
    talk("Qual a sua nota de 1 a 5?")
    assessment = take_command()
    print(assessment)
    bancoDeJogos.write("Avaliação: " + assessment)
    bancoDeJogos.write("\n")
    talk("Ok, jogo avaliado")


def tempo():
    """
    Função que fala o clima atual para saber se podemos sugerir um jogo em ar livre
    """
    API_KEY = os.getenv("API_KEY")
    cidade = 'são paulo'
    link = 'https://api.openweathermap.org/data/2.5/weather?appid=' + \
        API_KEY + '&q=' + cidade + '&lang=pt_br'
    print(link)
    requisicao = requests.get(link)
    print(requisicao)
    requisicao_dic = requisicao.json()
    print(requisicao_dic)
    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    clima = (
        f'A temperatura de agora é: {temperatura:.0f} º Celsius, com ' + descricao)
    print(clima)
    talk(clima)


# Lista de palavras que ativam suas respectivas funções
comandos = {
    'avaliar': lambda x: ratingGame(),
    'cadastrar': lambda x: newGame(),
    'criadores': lambda x: integrantes(),
    'tempo': lambda x: tempo(),
    'clima': lambda x: tempo(),
    'recomenda': lambda x: sugerirJogo(jogos),
    'sugira': lambda x: sugerirJogo(),

}


def run_almanak():
    """
    Função que recebe o comando e encaminha para sua determinada sessão, além disso ela também só 
    possibilita a passagem de comandos caso um usuário seja detectado e tenha falado a palavra de ativação
    """
    global ativo

    wake_call = take_command()
    if not "ok almanaque" in wake_call and len(detected_faces) > 0:
        return
    else:
        talk("Como posso ajudar?")
        print("Agora aceita comando")

        while True:
            command = take_command()
            print(command)
            for(key, value) in comandos.items():
                if key in command:
                    comandos[key](command)
                    break
            break


while True:
    run_almanak()
