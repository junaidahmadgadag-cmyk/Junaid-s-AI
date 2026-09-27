from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from config import Config
from search_tool import SearchTool


class ReactAgent:
    def __init__(self):
        # Create the search tool
        self.search_tool = SearchTool()

        # Store tools in a dictionary for easy access
        self.tools = {
            "search": self.search_tool
        }

        # Create Gemini model
        self.model = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.1,
        )

        # Give Gemini access to our tools
        self.model_with_tools = self.model.bind_tools(
            [self.search_tool]
        )

        # System instructions
        self.system_message = SystemMessage(
            content=(
                "You are Junaid's AI assistant. "
                "Give accurate, clear and useful answers. "
                "When the user asks for current, recent, live, "
                "or internet-based information, use the search tool. "
                "Do not use the search tool for simple questions "
                "that you can answer directly."
            )
        )

    def run(self, user_input: str) -> str:
        """
        Run the AI agent with the user's question.
        """

        messages = [
            self.system_message,
            HumanMessage(content=user_input)
        ]

        # Allow several tool-calling steps
        for _ in range(3):

            # Ask Gemini
            response = self.model_with_tools.invoke(messages)

            # Add Gemini response to conversation
            messages.append(response)

            # Check whether Gemini wants to use a tool
            if not response.tool_calls:
                return self._get_text(response)

            # Execute requested tools
            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})

                # Check if requested tool exists
                if tool_name not in self.tools:

                    tool_result = (
                        f"Error: tool '{tool_name}' does not exist."
                    )

                else:

                    try:
                        tool = self.tools[tool_name]

                        # Execute the tool
                        tool_result = tool.invoke(tool_args)

                    except Exception as e:

                        tool_result = (
                            f"Tool execution error: {str(e)}"
                        )

                # Send tool result back to Gemini
                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                )

        return (
            "I could not complete the request within the allowed "
            "number of steps."
        )

    def invoke(self, user_input: str) -> str:
        """
        Alternative method for calling the agent.
        """
        return self.run(user_input)

    @staticmethod
    def _get_text(response) -> str:
        """
        Extract text from Gemini's response.
        """

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            text_parts: List[str] = []

            for item in content:

                if isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        text_parts.append(text)

                elif isinstance(item, str):

                    text_parts.append(item)

            return "\n".join(text_parts)

        return str(content)


# Create the agent
agent = ReactAgent()


# Allow this file to be tested directly
if __name__ == "__main__":

    print("=" * 50)
    print("JUNAID AI AGENT")
    print("=" * 50)

    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower().strip() in ["exit", "quit"]:

            print("Goodbye!")
            break

        if not user_input.strip():

            continue

        try:

            answer = agent.run(user_input)

            print("\nAI:", answer)
            print()

        except Exception as e:

            print("\nError:", str(e))
            print()
