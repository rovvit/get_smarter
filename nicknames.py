import random

def GetRandomNickname(nickname_list):
    a = nickname_list[random.randint(1, len(nickname_list))]
    print(a)
    return a

def makeQuestion(nickname_list):
    nickname = GetRandomNickname(nickname_list)
    print(f'Кого называют таким прозивщем: {nickname[0]}?')
    answer = input()
    if answer.upper() == nickname[1].upper():
        print('правильно!')
    else:
        print(f'Дурак чтоле! Ответ же простой - {nickname[1]}')
