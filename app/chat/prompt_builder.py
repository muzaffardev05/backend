class PromptBuilder:

    @staticmethod
    def history(messages):

        text = ""

        for msg in messages:

            if msg.role == "user":

                text += f"User: {msg.content}\n"

            else:

                text += f"Assistant: {msg.content}\n"

        return text

    @staticmethod
    def documents(results):

        text = ""

        for i, tender in enumerate(results, start=1):

            text += f"""
Tender {i}

Title:
{tender['title']}

Organization:
{tender['organization']}

Location:
{tender['location']}

Closing:
{tender['closing_date']}

Status:
{tender['status']}



"""
        return text