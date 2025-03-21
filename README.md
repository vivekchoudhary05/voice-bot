# Voice-Enabled Gemini Chatbot

## Summary
This project is a voice-enabled chatbot that interacts with users using Google Gemini's generative AI. It supports speech recognition and text-to-speech capabilities, allowing for seamless spoken conversations. The chatbot extracts relevant information from a PDF resume and provides concise, structured responses based on the user's queries. It also maintains a limited history of previous questions to prevent repetition.

## Features
- **Speech Recognition**: Uses `speech_recognition` to capture and process voice input.
- **Text-to-Speech**: Converts chatbot responses to speech using `pyttsx3`.
- **Google Gemini API**: Generates AI-driven responses based on user queries.
- **PDF Resume Parsing**: Extracts and integrates resume details using `PyMuPDF (fitz)`.
- **Chat Memory**: Maintains a limited chat history (last 5 questions) to improve response consistency.

## Setup and Installation
### Prerequisites
Ensure you have Python installed (preferably 3.8+). Install the required dependencies:
```sh
pip install google-generativeai speechrecognition pyttsx3 pydub python-dotenv pymupdf
```

### API Key Configuration
1. Obtain a Gemini API key from Google.
2. Create a `.env` file in the project directory and add the following line:
   ```sh
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Chatbot
1. Place your resume PDF in the specified directory and update `resume_path` accordingly.
2. Run the chatbot:
   ```sh
   python main.py
   ```
3. Speak into the microphone when prompted. Say "exit" to end the conversation.

## Approach and Design Decisions
### 1. **Minimalist Chat Memory**
The chatbot stores only the last 5 user queries, preventing long-term memory accumulation but maintaining context for short conversations.

### 2. **Structured Personality with Custom Instructions**
The chatbot's behavior is defined by a system prompt that enforces conciseness, professionalism, and structured responses.

### 3. **PDF Resume Integration**
By extracting text from a resume, the chatbot can answer personalized questions about the user’s skills, experience, and background.

### 4. **Voice Interaction for Natural Conversations**
Speech recognition and text-to-speech components allow for hands-free interaction, making the chatbot more accessible and engaging.

### 5. **Error Handling for Robustness**
The program includes exception handling for:
   - Speech recognition failures (e.g., unclear input, service errors)
   - PDF extraction errors
   - API failures


### Author: Vivek Choudhary

