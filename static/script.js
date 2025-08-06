class VoiceAssistant {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        this.recordBtn = document.getElementById('recordBtn');
        this.status = document.getElementById('status');
        this.conversation = document.getElementById('conversation');
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.recordBtn.addEventListener('click', () => {
            if (!this.isRecording) {
                this.startRecording();
            } else {
                this.stopRecording();
            }
        });
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processAudio();
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            this.recordBtn.classList.add('recording');
            this.recordBtn.querySelector('.btn-text').textContent = 'Recording... Click to Stop';
            this.status.textContent = 'Listening... Speak now!';
            
        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.status.textContent = 'Error: Could not access microphone';
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            this.recordBtn.classList.remove('recording');
            this.recordBtn.querySelector('.btn-text').textContent = 'Click to Speak';
            this.status.textContent = 'Processing your question...';
            
            // Stop all audio tracks
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    async processAudio() {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        
        try {
            const response = await fetch('/process-audio', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.displayError(result.error);
            } else {
                this.displayConversation(result.question, result.answer);
            }
            
        } catch (error) {
            console.error('Error processing audio:', error);
            this.displayError('Failed to process your question. Please try again.');
        }
        
        this.status.textContent = 'Ready to listen...';
    }
    
    displayConversation(question, answer) {
        // Clear example questions if they exist
        const examples = this.conversation.querySelector('.example-questions');
        if (examples) {
            examples.remove();
        }
        
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerHTML = `<strong>You:</strong> ${question}`;
        this.conversation.appendChild(userMessage);
        
        // Add bot response
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        botMessage.innerHTML = `<strong>AI:</strong> ${answer}`;
        this.conversation.appendChild(botMessage);
        
        // Scroll to bottom
        this.conversation.scrollTop = this.conversation.scrollHeight;
    }
    
    displayError(errorMessage) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = `Error: ${errorMessage}`;
        this.conversation.appendChild(errorDiv);
    }
}

// Initialize the voice assistant when page loads
document.addEventListener('DOMContentLoaded', () => {
    new VoiceAssistant();
});
