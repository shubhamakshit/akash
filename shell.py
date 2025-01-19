from prompt_toolkit import PromptSession
from glv import Global

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion.filesystem import PathCompleter
from prompt_toolkit.document import Document


class CustomCompleter(Completer):
    def __init__(self):
        self.file_completer = PathCompleter()

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        if text.startswith('cd '):
            for completion in self.file_completer.get_completions(document, complete_event):
                yield completion


def main():
    # Initialize Prompt Toolkit session
    session = PromptSession()

    # Add a custom completer
    custom_completer = CustomCompleter()

    from shellLogic import logic

    # Command-line interface loop
    while True:
        try:
            user_input = session.prompt('|aakash-dl> ', completer=custom_completer)

            # just in case the user hits enter without typing anything
            if not user_input: continue

            command = user_input.split()[0]
            args = user_input.split()[1:]
            if not args: args = []

            try:
                # check if first arg is /? or -h or --help
                if args and args[0] in ['/?', '-h', '--help']:
                    logic.execute_help(command)
                else:
                    logic.execute(command, args)
            except Exception as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except SystemExit:
            if command == 'exit':
                break


if __name__ == "__main__":
    main()
