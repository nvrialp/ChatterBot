import yaml
import spacy
import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from itertools import chain

nlp = spacy.load('es_core_news_lg')
yaml_file = "conversations+greetings-cgpt.yaml"

with open(yaml_file, 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

conversations = data['conversations']
categories = data.get('categories', [])

chatbot = ChatBot(
    'Kourtney',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.SpacySimilarity',
            'default_response': 'Lo siento, no entiendo.',
            'maximum_similarity_threshold': 0.70
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.JaccardSimilarity',
            'default_response': 'Lo siento, no entiendo.',
            'maximum_similarity_threshold': 0.50
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.LevenshteinDistance',
            'default_response': 'Lo siento, no entiendo.',
            'maximum_similarity_threshold': 0.60
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ],
    database_uri='sqlite:///database2.sqlite3'
)


trainer = ListTrainer(chatbot)
trainer.train(yaml_file)


def Best_Answer(input_text):
    doc_input = nlp(input_text)
    best_score = 0
    best_answer = "No estoy seguro de cómo responder a eso."

    for conversation in conversations:
        question = conversation[0]
        answers = conversation[1:]
        doc_question = nlp(question)
        similarity_question = doc_input.similarity(doc_question)

        if similarity_question > best_score:
            best_score = similarity_question
            best_answer = random.choice(answers)

        for answer in answers:
            doc_answer = nlp(answer)
            similarity_answer = doc_input.similarity(doc_answer)
            if similarity_answer > best_score:
                best_score = similarity_answer
                best_answer = answer
    if best_score > 0.4:
        best_answer = best_answer
    elif best_score < 0.3:
        best_answer = "No estoy seguro de cómo responder a eso. ¿Podrías darme más contexto?"
    return best_answer


print("🤖 Escribe 'salir' o 'adiós' para terminar.")
while True:
    try:
        user_input = input("Tú: ")
        if user_input.lower() in ['adiós', 'salir']:
            print("Bot: ¡Hasta luego!")
            break

        response = chatbot.get_response(user_input)
        print(f"Bot (ChatterBot): {response}")
        print(f"Confianza: {response.confidence:.2f}")

        if response.text == 'Lo siento, no entiendo.':
            print("Bot: Intentaré con otra estrategia...")
            respuesta_spacy = Best_Answer(user_input)
            print(f"Bot (spaCy): {respuesta_spacy}")

    except (KeyboardInterrupt, EOFError, SystemExit):
        break