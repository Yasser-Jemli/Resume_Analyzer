import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment'; // Import environment for API key

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.css']
})
export class ChatBotComponent {
  messages: { sender: string; text: string }[] = [];
  userInput: string = '';
  apiUrl: string = 'https://api.x.ai/v1/chat/completions'; // Correct xAI Grok API endpoint

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.userInput.trim()) return;

    // Add user message to the chat
    this.messages.push({ sender: 'User', text: this.userInput });

    // Prepare the payload for xAI Grok API
    const payload = {
      model: 'grok-beta', // Use xAI's Grok model
      messages: [
        { role: 'system', content: 'You are Grok, a helpful AI assistant created by xAI.' },
        { role: 'user', content: this.userInput }
      ]
    };

    // Set headers with xAI API key from environment
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${environment.xaiApiKey}` // Securely load API key
    });

    // Send the message to the xAI Grok API
    this.http
      .post<{ choices: { message: { content: string } }[] }>(this.apiUrl, payload, { headers })
      .subscribe({
        next: (response) => {
          // Add chatbot reply to the chat
          const botReply = response.choices[0].message.content;
          this.messages.push({ sender: 'Bot', text: botReply });
        },
        error: (error) => {
          console.error('Error communicating with xAI Grok API:', error);
          let errorMessage = 'Sorry, I am unable to respond at the moment.';
          if (error.status === 429) {
            errorMessage = 'Rate limit exceeded. Please try again later.';
          } else if (error.status === 403) {
            errorMessage = 'Authentication failed. Please check your API key.';
          }
          this.messages.push({ sender: 'Bot', text: errorMessage });
        }
      });

    // Clear the input field
    this.userInput = '';
  }
}