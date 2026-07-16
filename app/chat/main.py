from app.chat.chatbot import ChatBot
from app.services.database_service import DatabaseService


def main():

    bot = ChatBot()
    db = DatabaseService()

    user_id = 1

    session = db.create_session(
        user_id=user_id,
        title="New Chat"
    )

    print(f"Session ID: {session.id}")

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        # Save user message
        db.save_message(
            session_id=session.id,
            role="user",
            content=question
        )

        response = bot.ask(question)

        answer = response["answer"]

        print("\nAssistant:\n")
        print(answer)

        # Save assistant message
        db.save_message(
            session_id=session.id,
            role="assistant",
            content=answer
        )


if __name__ == "__main__":
    main()