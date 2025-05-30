class ChatMemory:
    """
    Class to manage chatbot conversation history.
    Stores user inputs and chatbot responses.
    """
    def __init__(self):
        self.history = []

    def add_message(self, user_message, bot_response):
        """
        Adds a new user-bot message pair to the conversation history.
        """
        self.history.append({"user": user_message, "bot": bot_response})

    def get_history(self):
        """
        Returns the full conversation history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the entire conversation history.
        """
        self.history = []

    def get_context(self):
        """
        Returns the conversation history as a formatted string to use as context.
        """
        context = ""
        for entry in self.history:
            context += f"User: {entry['user']}\nBot: {entry['bot']}\n"
        return context
