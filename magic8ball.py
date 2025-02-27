import random
import time
import json
from datetime import datetime
from colorama import Fore, Back, Style, init
import sys

init(autoreset=True)  # Initialize colorama

class Magic8Ball:
    def __init__(self):
        self.responses = {
            'positive': [
                "Yes - Definitely.", "It is decidedly so.", "Without a doubt.",
                "Yes, absolutely.", "You may rely on it.", "As I see it, yes.",
                "Most likely.", "Outlook good.", "Yes.", "Signs point to yes."
            ],
            'neutral': [
                "Reply hazy, try again.", "Ask again later.",
                "Better not tell you now.", "Cannot predict now.",
                "Concentrate and ask again."
            ],
            'negative': [
                "Don't count on it.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Very doubtful."
            ]
        }
        self.history = []
        self.stats = {'positive': 0, 'neutral': 0, 'negative': 0}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = datetime.now().isoformat()  # Session start time
        
    def _get_answer(self, question):
        """Select an answer and update statistics"""
        category = random.choices(
            population=['positive', 'neutral', 'negative'],
            weights=[0.4, 0.3, 0.3],
            k=1
        )[0]
        answer = random.choice(self.responses[category])
        self.stats[category] += 1
        self.history.append({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        return answer

    def _show_animation(self):
        """Display shaking animation with progress bar"""
        symbols = ['●', '○', '◎', '◇', '☆']
        print(Fore.CYAN + "\nShaking the Magic 8 Ball...")
        for i in range(5):
            time.sleep(0.3)
            sys.stdout.write(f"\r[{''.join(random.choices(symbols, k=10))}]")
            sys.stdout.flush()
        print("\n")

    def _show_welcome(self):
        """Display welcome message with ASCII art"""
        print(Fore.MAGENTA + r"""
    ╔═══╗─────────╔╗
    ║╔═╗║─────────║║
    ║╚══╦╗╔╦══╦══╗║║╔══╗
    ╚══╗║╚╝║╔╗║╔═╝║║║══╣
    ║╚═╝║║║║╚╝║╚═╗║╚╬══║
    ╚═══╩╩╩╩══╩══╝╚═╩══╝
        """)
        print(Fore.CYAN + "=== Advanced Magic 8 Ball ===")
        print(Fore.YELLOW + "Type '/help' for commands\n")

    def _save_session(self):
        """Save session data to JSON file"""
        filename = f"8ball_session_{self.session_id}.json"
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'session_id': self.session_id,
                    'start_time': self.start_time,
                    'end_time': datetime.now().isoformat(),
                    'total_questions': len(self.history),
                    'stats': self.stats,
                    'history': self.history
                }, f, indent=2)
            print(Fore.GREEN + f"\nSession saved to {filename}")
        except Exception as e:
            print(Fore.RED + f"\nError saving session: {str(e)}")

    def _show_help(self):
        """Display help information"""
        print(Fore.YELLOW + "\nAvailable commands:")
        print("  /help    - Show this help message")
        print("  /history - Show question history")
        print("  /stats   - Display answer statistics")
        print("  /exit    - Quit the application\n")

    def main(self):
        self._show_welcome()
        
        while True:
            question = input(Fore.WHITE + "\nAsk a Yes/No question: ").strip()
            
            if not question:
                continue
                
            # Handle commands
            if question.startswith('/'):
                if question == '/exit':
                    self._save_session()
                    print(Fore.MAGENTA + "\nThanks for playing! Goodbye! ✨")
                    break
                elif question == '/help':
                    self._show_help()
                elif question == '/history':
                    print(Fore.CYAN + "\nQuestion History:")
                    for idx, entry in enumerate(self.history, 1):
                        print(f"{idx}. [{entry['timestamp'][11:19]}] "
                              f"Q: {entry['question']}\n   A: {entry['answer']}")
                elif question == '/stats':
                    print(Fore.GREEN + "\nAnswer Statistics:")
                    total = sum(self.stats.values())
                    if total == 0:
                        print("No answers yet!")
                        continue
                    for cat, count in self.stats.items():
                        pct = (count / total * 100)
                        print(f"{cat.title()}: {count} ({pct:.1f}%)")
                continue

            # Handle question
            self._show_animation()
            answer = self._get_answer(question)
            time.sleep(0.5)
            print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " The Oracle Speaks ".center(40, '✨'))
            print(Style.RESET_ALL + Fore.CYAN + f"\n   {answer}\n")
            print(Style.RESET_ALL + "-"*40)

if __name__ == "__main__":
    app = Magic8Ball()
    try:
        app.main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nSession interrupted. Saving progress...")
        app._save_session()
