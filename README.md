# Discord Bot

A feature-rich Discord bot with moderation, fun, and utility commands.

## Features

- **Fun Commands**: 8ball, who, vibecheck, roll dice
- **Utility Commands**: clear messages, user info, server info

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. **Important**: Enable Privileged Intents (optional)
   - Go to [Discord Developer Portal](https://discord.com/developers/applications/)
   - Select your application
   - Go to "Bot" tab
   - Enable "Server Members Intent" and "Message Content Intent" under "Privileged Gateway Intents"
   - If you enable these, update the bot code to set `intents.members = True` in main.py and bot.py
   
5. Run the bot:
   ```
   python main.py
   ```

## Commands

### Fun Commands
- `!8ball <question>` - Ask a yes/no question
- `!who <question>` - Ask who will do something
- `!vibecheck <subject>` - Check someone's vibe
- `!roll [NdN]` - Roll dice (default: 1d6)

### Utility Commands
- `!clear [amount]` - Clear messages from the channel (default: 5)
- `!userinfo [member]` - Get information about a user
- `!serverinfo` - Get information about the server
- `!say <message>` - Make the bot say something

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
