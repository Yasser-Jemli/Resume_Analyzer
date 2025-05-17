import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat-assistant',
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent {
  messages: { sender: string; text: string; audioUrl?: string }[] = [];
  userInput: string = '';

  constructor(private http: HttpClient) {}

  sendMessage(): void {
    const input = this.userInput.trim();
    if (!input) return;

    this.messages.push({ sender: 'Vous', text: input });

    this.http.post<{ text: string; audio_url?: string }>('/ask', { user_input: input }).subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.text, audioUrl: res.audio_url });
        this.userInput = '';

        // Si audio disponible, jouer le son
        if (res.audio_url) {
          const audio = new Audio(res.audio_url);
          audio.play();
        }
      },
      error: () => {
        this.messages.push({ sender: 'Bot', text: 'Erreur lors de la communication avec le serveur.' });
      }
    });
  }
}
