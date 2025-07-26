# jamtime
![Hackatime Badge](https://hackatime-badge.hackclub.com/U091H0MHT2B/jamtime?label=Time%20Wasted&style=for-the-badge)
![Pycord Badge](https://img.shields.io/badge/made_with-pycord-%237289da?style=for-the-badge&logo=discord&labelColor=%23424549)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/snqwq/jamtime?style=for-the-badge)
![Black Badge](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)
![Autism Badge](https://img.shields.io/badge/powered_by-evil_autism-%23de3449?style=for-the-badge)

Discord bot for staying productive and timing game jams, projects, or really anything tbh

Written in python using the [Pycord](https://pycord.dev) library

## Goals

### v1.0 (first release)
- [x] Basic timer functionality (start, stop, alerts, etc.)
- [x] Slash commands
- [x] Persistent timers
- [x] Subscription system (you can subscribe to other people's timers)
- [x] ID and short ID system for timers
- [x] Automatic notifications (half way and end)
- [x] Functions in dms
- [x] Functions in servers
- [ ] ~24/7 uptime/officially hosted somewhere
- [x] Actually be useful
- [ ] Awesome cool demo video


### v2.0 (next release)
- [ ] Pomodoro timer
- [ ] Customizable timer reminders (not just half way and end)
- [ ] customizable timer messages (like "TIMER IS OVER!!!" or whatever the user wants)
- [ ] Project functionality
- [ ] Hackatime integration (for tracking time spent on projects)
- [ ] Change database to not just be a json file (use sqlite or something)
- [ ] Replace task system with a queue system and try to keep more stuff in memory
- [ ] Statistics command
- [ ] Timer pause/resume functionality
- [ ] Timer notes/descriptions
- [ ] Timer tags for organization
- [ ] Timer searching
- [ ] Scheduled timers (like "start timer at 3pm" or "start timer on 1st of January")
- [ ] Natural language processing for timer commands (timer new 12 minutes, timer new 1879007624, timer new friday at 3pm, etc.)
- [ ] Timer history (like "all timers last 5 weeks")


### v3.0 (future release)
- [ ] Timer categories (game jam, project, etc.)
- [ ] Timer types (stopwatch, repeating, countdown, etc.)
- [ ] Itch.io integration for gamejams (kinda funny how like half of the name is jam and the jam feature is like a far future thing)
- [ ] Google calendar integration (for scheduling timers)
- [ ] Progress bars or other live visualizations of timers

# Usage

Either [invite the bot to your server](https://discord.com/oauth2/authorize?client_id=1389020970739826799&permissions=17602923513856&integration_type=0&scope=bot) or dm it if you are in a server with it, then you can use the slash commands.

# Installation

*only for if you want to run the bot yourself, otherwise you can just invite it to your server or dm it*

## requirements
- Python 3.12.1 (might work on other versions, but not tested)
- git (only if you want to clone the repo)

1. Clone the repository and cd into it:
    ```bash
    git clone https://github.com/snqwq/jamtime.git
    cd jamtime
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Discord bot token:
    ```env
    DISCORD_TOKEN=your_token_here
    ```

5. Change any configs in `config.py` as needed (e.g., `IS_DEV = False` if you want to run in production mode or changing `DB_PATH` to a different location)

6. Run the bot:
    ```bash
    python bot.py
    ```
7. If you want to run the bot on startup on Linux, you can set that up using `helpers/setup_linux.sh` (make sure to run it with `chmod +x helpers/setup_linux.sh` first)

8. Enjoy! 🎉