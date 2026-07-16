from app.chat.chatbot import ChatBot
from app.services.database_service import DatabaseService


def print_menu():
    print("\n==============================")
    print("Tender AI Chat")
    print("==============================")
    print("1. Continue latest chat")
    print("2. Start new chat")
    print("3. List all chats")
    print("4. Open chat by Session ID")
    print("5. Exit")
    print("==============================")


def chat_loop(bot, db, session):

    print(f"\nCurrent Session: {session.id}")
    print("Type 'back' to return to the menu.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "back":
            break

        if question == "":
            continue

        db.save_message(
            session_id=session.id,
            role="user",
            content=question
        )

        response = bot.ask(question)

        answer = response["answer"]

        print("\nAssistant:\n")
        print(answer)
        print()

        db.save_message(
            session_id=session.id,
            role="assistant",
            content=answer
        )


def main():

    bot = ChatBot()
    db = DatabaseService()

    user_id = 1

    while True:

        print_menu()

        choice = input("Select option: ").strip()

        # Continue latest chat
        if choice == "1":

            session = db.get_latest_session(user_id)

            if session is None:

                print("\nNo previous chat found.")
                print("Creating a new one...\n")

                session = db.create_session(
                    user_id=user_id,
                    title="New Chat"
                )

            chat_loop(bot, db, session)

        # New chat
        elif choice == "2":

            session = db.create_session(
                user_id=user_id,
                title="New Chat"
            )

            chat_loop(bot, db, session)

        # List sessions
        elif choice == "3":

            sessions = db.get_sessions(user_id)

            if not sessions:
                print("\nNo chats found.\n")
                continue

            print()

            for s in sessions:
                print(
                    f"ID: {s.id} | "
                    f"Title: {s.title} | "
                    f"Updated: {s.updated_at}"
                )

        # Open specific session
        elif choice == "4":

            session_id = input("Session ID: ")

            if not session_id.isdigit():
                print("Invalid Session ID")
                continue

            session = db.get_session(int(session_id))

            if session is None:
                print("Session not found.")
                continue

            chat_loop(bot, db, session)

        elif choice == "5":
            break

        else:
            print("Invalid option.")

    db.close()


if __name__ == "__main__":
    main()