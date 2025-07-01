import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat-assistant',
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent {
  messages: { sender: string; text: string; audioUrl?: string }[] = [];
  userInput: string = '';
  loading: boolean = false;
  isOpen: boolean = false;

  @ViewChild('chatBody') chatBodyRef!: ElementRef;

  constructor(private http: HttpClient) {}

  toggleChat(): void {
    this.isOpen = !this.isOpen;
    setTimeout(() => this.scrollToBottom(), 100);
  }

  sendMessage(): void {
    const input = this.userInput.trim();
    if (!input) return;

    this.messages.push({ sender: 'Vous', text: input });
    this.userInput = '';
    this.scrollToBottom();
    this.loading = true;

    this.http.post<{ answer: string; audio_url?: string }>('/ask-assis', { question: input }).subscribe({
      next: res => {
        console.log('Réponse reçue:', res);
        this.messages.push({ sender: 'Bot', text: res.answer, audioUrl: res.audio_url });
        this.loading = false;
        this.scrollToBottom();
        if (res.audio_url) {
          const audio = new Audio(res.audio_url);
          audio.play();
        }
      },
      error: err => {
        console.error('Erreur serveur:', err);
        this.messages.push({ sender: 'Bot', text: '❌ Erreur serveur.' });
        this.loading = false;
        this.scrollToBottom();
      }
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.chatBodyRef && this.chatBodyRef.nativeElement) {
        this.chatBodyRef.nativeElement.scrollTop = this.chatBodyRef.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
