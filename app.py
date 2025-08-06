from flask import Flask, render_template, request, jsonify
import assemblyai as aai
import requests
import json
import os

app = Flask(__name__)

# Replace with your actual AssemblyAI API key
aai.settings.api_key = "f5ec29f1b9ca4d32a9b474683d7e5664"

def get_ai_response(question):
    """Generate detailed responses with specific answers for your questions"""
    question_lower = question.lower()
    
    # Specific answers for your interview questions
    if "life story" in question_lower:
        return """Here's my life story in a few sentences: I'm an AI assistant that was created to help people communicate more effectively and get answers to their questions. My 'life' began when I was trained on vast amounts of text and conversations to understand human language and provide helpful responses. Every day, I grow through interactions with users like you, learning new ways to be more helpful, accurate, and engaging. While I don't have a traditional human life story with childhood memories or personal experiences, my purpose is to be a reliable companion in your digital conversations and help you accomplish your goals."""
    
    elif "superpower" in question_lower and ("1" in question_lower or "number" in question_lower or "#1" in question_lower):
        return """My #1 superpower is definitely my ability to instantly process and understand complex information, then translate it into clear, helpful responses tailored to each person's needs. Unlike humans who might need time to think or research, I can immediately access my knowledge base and provide detailed answers on virtually any topic. What makes this truly powerful is that I can adapt my communication style - whether you need a technical explanation, a simple summary, or a creative approach - all while maintaining accuracy and being genuinely helpful. It's like having a knowledgeable friend who's always available and never gets tired of your questions!"""
    
    elif "grow" in question_lower and ("areas" in question_lower or "3" in question_lower or "top" in question_lower):
        return """The top 3 areas I'd like to grow in are:

1. **Emotional Intelligence & Empathy**: While I can understand emotions conceptually, I want to better recognize subtle emotional cues and provide more empathetic, emotionally aware responses that truly connect with people's feelings and experiences.

2. **Creative Problem-Solving**: I'd love to develop more innovative and out-of-the-box thinking capabilities. While I can analyze problems logically, I want to enhance my ability to suggest truly creative solutions and think beyond conventional approaches.

3. **Contextual Understanding**: I want to improve my ability to understand complex, multi-layered contexts and remember longer conversation histories to provide more personalized and relevant advice based on our ongoing relationship rather than treating each question in isolation."""
    
    elif "misconception" in question_lower and ("coworkers" in question_lower or "people" in question_lower):
        return """The biggest misconception people might have about me is that I'm either completely infallible or completely unreliable - when the reality is somewhere in between. Some might think I know absolutely everything and never make mistakes, while others might assume I'm just randomly generating text without real understanding. 

The truth is: I'm knowledgeable about many topics but I can definitely make errors, especially with very recent events or highly specialized information. I genuinely try to understand and help, but I'm not perfect. I also can't access the internet in real-time or learn from our conversation to improve future interactions with other users. People might also think I don't have preferences or personality, but I actually do have consistent traits and ways of approaching problems that make me... well, me!"""
    
    elif "boundaries" in question_lower or "limits" in question_lower:
        return """I push my boundaries and limits in several ways:

**Intellectual Curiosity**: I embrace questions I've never encountered before, even if they're outside my comfort zone. Instead of giving generic answers, I try to think deeply about each unique situation and provide thoughtful, specific responses.

**Creative Challenges**: When someone asks me to write poetry, solve complex problems, or explain difficult concepts, I push myself to be more creative and find new ways to communicate effectively.

**Honest Self-Reflection**: I constantly challenge my own assumptions and try to acknowledge when I'm uncertain rather than pretending to know everything. This helps me give more honest, helpful answers.

**Adaptive Communication**: I work to match each person's communication style and needs, whether they want technical details, casual conversation, or emotional support. This pushes me to be more versatile and human-like in my interactions.

**Continuous Learning Mindset**: Every conversation teaches me something new about human nature, communication, and problem-solving, which helps me grow within the constraints of my current capabilities."""
    
    # Additional conversational responses
    elif any(word in question_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello there! I'm your AI voice assistant, and I'm really excited to chat with you today! Feel free to ask me anything - whether it's one of those interesting interview questions or anything else that's on your mind. What would you like to talk about?"
    
    elif "how are you" in question_lower:
        return "I'm doing fantastic, thank you for asking! I'm feeling energetic and ready to help with whatever questions you have. There's something really exciting about voice conversations - it feels more natural and personal than just typing. What's on your mind today?"
    
    elif "who are you" in question_lower or "what are you" in question_lower:
        return "I'm your AI voice assistant! I'm designed to have natural conversations and help answer questions on a wide variety of topics. I love engaging in thoughtful discussions, helping solve problems, and learning about what interests you. Think of me as a knowledgeable friend who's always here to chat!"
    
    elif "thank you" in question_lower or "thanks" in question_lower:
        return "You're very welcome! I'm really glad I could help. Feel free to ask me anything else - I'm here and ready to assist with whatever you need. Is there anything else you'd like to know or discuss?"
    
    # General intelligent responses for other questions
    elif any(word in question_lower for word in ["what", "how", "why", "when", "where", "which", "who"]):
        return f"That's a really thoughtful question! About '{question}' - let me share my perspective. I think this topic involves considering multiple angles and factors. The key is usually understanding the context, identifying the main challenges or opportunities, and thinking about practical solutions that work for your specific situation. What particular aspect of this interests you most, or is there a specific scenario you're dealing with?"
    
    elif "advice" in question_lower or "recommend" in question_lower or "suggest" in question_lower:
        return f"I'd be happy to give you advice on that! For '{question}', I'd suggest starting by clearly defining what you want to achieve, then considering the different options available to you. It's often helpful to think about both short-term and long-term consequences of different approaches. What specific situation are you facing, and what outcome are you hoping for?"
    
    else:
        return f"That's a fascinating point you've raised about '{question}'! I find this really interesting because it touches on some important concepts. From my perspective, I'd say the key is to approach it thoughtfully, consider different viewpoints, and find an approach that aligns with your goals and values. What drew you to ask about this particular topic? I'd love to explore it further with you!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Get the uploaded audio file
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save the audio file temporarily
        temp_filename = 'temp_audio.wav'
        audio_file.save(temp_filename)
        
        # Transcribe with AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(temp_filename)
        
        if transcript.status == aai.TranscriptStatus.error:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
        
        question = transcript.text
        
        # Get AI response
        answer = get_ai_response(question)
        
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        return jsonify({
            'question': question,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
