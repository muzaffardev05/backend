from app.chat.chatbot import ChatBot


def main():

    bot = ChatBot()

    while True:

        question = input("\nYou : ")

        if question.lower() in [
            "exit",
            "quit"
        ]:
            break

        response = bot.ask(question)

        print("\nAssistant:\n")

        print(response["answer"])


if __name__ == "__main__":

    main()