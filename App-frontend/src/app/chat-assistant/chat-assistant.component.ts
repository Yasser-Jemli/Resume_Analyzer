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

    this.http.post<{ text: string; audio_url?: string }>('/ask', { user_input: input }).subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.text, audioUrl: res.audio_url });
        this.loading = false;
        this.scrollToBottom();
        if (res.audio_url) {
          const audio = new Audio(res.audio_url);
          audio.play();
        }
      },
      error: () => {
        this.messages.push({ sender: 'Bot', text: '❌ Erreur serveur.' });
        this.loading = false;
        this.scrollToBottom();
      }
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.chatBodyRef?.nativeElement) {
        this.chatBodyRef.nativeElement.scrollTop = this.chatBodyRef.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
