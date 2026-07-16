from app.chat.chatbot import ChatBot
from app.services.database_service import DatabaseService


class AssistantService:

    def __init__(self):

        self.bot = ChatBot()
        self.db = DatabaseService()

    def close(self):
        self.db.close()



    def chat(self, user_id, message, session_id=None):

        if session_id is None:

            session = self.db.create_session(
                user_id=user_id,
                title="New Chat"
            )

        else:

            session = self.db.get_session(session_id)

            if session is None:
                raise Exception("Session not found")

        self.db.save_message(
            session.id,
            "user",
            message
        )

        response = self.bot.ask(message)

        answer = response["answer"]

        self.db.save_message(
            session.id,
            "assistant",
            answer
        )

        return {
            "session_id": session.id,
            "answer": answer,
            "sources": response.get("sources", [])
        }        

    def get_sessions(self, user_id):

        sessions = self.db.get_sessions(user_id)

        return {
            "sessions": [
                {
                    "id": session.id,
                    "title": session.title,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at
                }
                for session in sessions
            ]
        }    


    def get_conversation(self, session_id):

        session = self.db.get_session(session_id)

        if session is None:
            raise Exception("Session not found")

        messages = self.db.get_messages(session_id)

        return {
            "session_id": session.id,
            "title": session.title,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at
                }
                for message in messages
            ]
        }    


    def delete_session(self, session_id):

        deleted = self.db.delete_session(session_id)

        if not deleted:
            raise Exception("Session not found")

        return {
            "message": "Session deleted successfully."
    }