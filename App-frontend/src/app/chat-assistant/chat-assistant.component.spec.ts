import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat-assistant',
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent {
  messages: { sender: string; text: string }[] = [];
  userInput = '';

  constructor(private http: HttpClient) {}

  sendMessage(): void {
    const input = this.userInput.trim();
    if (!input) return;

    this.messages.push({ sender: 'Vous', text: input });

    this.http.post<{ response: string }>('/entretien-ask', { user_input: input }).subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.response });
        this.userInput = '';
      },
      error: err => {
        this.messages.push({ sender: 'Bot', text: 'Erreur lors de la communication avec le serveur.' });
      }
    });
  }
}
