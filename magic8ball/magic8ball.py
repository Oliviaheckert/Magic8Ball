import random
import time
import json
import logging.config
from datetime import datetime
from colorama import Fore, Back, Style, init
import sys

init(autoreset=True)  # Initialize colorama

class Magic8Ball:
    def __init__(self):
        # Configure logging
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize responses and tracking
        self.responses = self._load_responses()
        self.history = []
        self.stats = {'positive': 0, 'neutral': 0, 'negative': 0}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = datetime.now().isoformat()

    def _load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "weights": {"positive": 0.4, "neutral": 0.3, "negative": 0.3},
            "animation": {"symbols": ["●","○"], "delay": 0.3, "cycles": 5}
        }
        
        try:
            with open('config/settings.json') as f:
                config = json.load(f)
                self.logger.info("Successfully loaded configuration")
                return config
        except FileNotFoundError:
            self.logger.warning("Config file not found, using defaults")
            return default_config
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON config: {str(e)}")
            return default_config

    def _load_responses(self):
        """Load responses from configuration"""
        try:
            with open('config/responses.json') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Response file missing, using built-in responses")
            return {
                'positive': ["Yes - Definitely.", "It is decidedly so."],
                'neutral': ["Reply hazy, try again."],
                'negative': ["Don't count on it."]
            }

    def _get_answer(self, question):
        """Select an answer using configured weights"""
        try:
            weights = [
                self.config['weights']['positive'],
                self.config['weights']['neutral'],
                self.config['weights']['negative']
            ]
            category = random.choices(
                population=['positive', 'neutral', 'negative'],
                weights=weights,
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
            
        except KeyError as e:
            self.logger.error(f"Configuration error: {str(e)}")
            return "Error in configuration, please check settings"

    def _show_animation(self):
        """Display animation using configured parameters"""
        try:
            symbols = self.config['animation']['symbols']
            delay = self.config['animation']['delay']
            cycles = self.config['animation']['cycles']
            
            print(Fore.CYAN + "\nShaking the Magic 8 Ball...")
            for i in range(cycles):
                time.sleep(delay)
                sys.stdout.write(f"\r[{''.join(random.choices(symbols, k=10))}]")
                sys.stdout.flush()
            print("\n")
            
        except KeyError as e:
            self.logger.error(f"Animation config error: {str(e)}")
            print("\n** Shaking animation disabled **\n")

    def _save_session(self):
        """Save session data with error handling"""
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
                
            self.logger.info(f"Session saved to {filename}")
            print(Fore.GREEN + f"\nSession saved to {filename}")
            
        except (IOError, PermissionError) as e:
            self.logger.error(f"File save error: {str(e)}")
            print(Fore.RED + f"\nError saving session: {str(e)}")
        except json.JSONEncodeError as e:
            self.logger.error(f"JSON encoding error: {str(e)}")
            print(Fore.RED + "\nError encoding session data")

    # Rest of the methods remain similar but use logger instead of print for system messages
    # ... [Other methods like _show_welcome, _show_help, main etc.] ...

if __name__ == "__main__":
    try:
        app = Magic8Ball()
        app.main()
    except KeyboardInterrupt:
        app.logger.info("Session interrupted by user")
        print(Fore.RED + "\n\nSession interrupted. Saving progress...")
        app._save_session()
    except Exception as e:
        app.logger.critical(f"Critical error: {str(e)}", exc_info=True)
        print(Fore.RED + "\nA critical error occurred. Check logs for details.")
