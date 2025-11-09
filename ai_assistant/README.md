# AI Assistant Collection

A comprehensive collection of AI-powered voice and text assistants with different capabilities and interfaces.

## 🚀 Quick Start

1. **Setup**: Run `python setup.py` to install dependencies
2. **Configure**: Update `config.py` with your API keys
3. **Launch**: Run `python launcher.py` to choose an assistant

## 🤖 Available Assistants

### 1. Experiment Jarvis (`experiment_jarvis.py`)
- **Features**: Voice commands, web browsing, app launching, time telling
- **Best for**: General purpose voice assistant
- **Commands**: 
  - "open youtube/google/github"
  - "what time is it"
  - "play music"
  - "open chrome/cursor/linux"

### 2. Jarvis GUI (`jarvis-generation-2/gui.py`)
- **Features**: Graphical interface, voice + text input, news updates
- **Best for**: Users who prefer GUI interaction
- **Special**: Real-time chat interface with voice recognition

### 3. Jarvis Max (`jarvis-max/main.py`)
- **Features**: Lightweight, app/website launcher
- **Best for**: Simple automation tasks
- **Commands**: "open [app/website name]"

### 4. Gemini AI (`gemini ai/gemini-ai.py`)
- **Features**: Advanced multimodal AI with camera/screen sharing
- **Best for**: Advanced AI interactions with visual input
- **Modes**: Camera, screen capture, text-only

## 🔧 Configuration

### API Keys Required:
- **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **News API**: Get from [NewsAPI.org](https://newsapi.org/)

### Update `config.py`:
```python
GEMINI_API_KEY = "your_actual_api_key_here"
NEWS_API_KEY = "your_news_api_key_here"
```

## 📋 Dependencies

All dependencies are automatically installed via `setup.py`:
- `google-generativeai` - Gemini AI integration
- `pyttsx3` - Text-to-speech
- `speechrecognition` - Voice recognition
- `pyautogui` - GUI automation
- `opencv-python` - Computer vision
- `tkinter` - GUI framework

## 🎯 Usage Examples

### Voice Commands:
- "Jarvis, open YouTube"
- "What time is it?"
- "Play some music"
- "Send a message"
- "Open Chrome"
- "Jarvis shutdown"

### Text Commands:
- Type in GUI or console
- Same commands as voice
- More precise for complex queries

## 🛠️ Troubleshooting

### Common Issues:

1. **Microphone not working**:
   - Check Windows microphone permissions
   - Ensure microphone is set as default device

2. **API errors**:
   - Verify API keys in `config.py`
   - Check internet connection
   - Ensure API quotas aren't exceeded

3. **Import errors**:
   - Run `python setup.py` again
   - Check Python version (3.7+ required)

4. **GUI not opening**:
   - Ensure tkinter is installed
   - Check display settings

### Performance Tips:
- Close unnecessary applications for better voice recognition
- Use wired microphone for better accuracy
- Ensure stable internet for AI features

## 🔒 Security Notes

- API keys are stored locally in `config.py`
- No data is stored permanently
- Voice data is processed by Google Speech API
- Gemini AI processes text/images according to Google's privacy policy

## 🤝 Contributing

Feel free to:
- Add new voice commands
- Improve error handling
- Add new AI assistant variants
- Enhance GUI design

## 📝 License

This project is for educational and personal use.

---

**Note**: Make sure to keep your API keys secure and never commit them to version control.