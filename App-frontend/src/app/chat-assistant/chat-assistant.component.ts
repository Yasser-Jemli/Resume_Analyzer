import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { finalize } from 'rxjs/operators';

interface ChatMessage {
  sender: 'Vous' | 'Bot';
  text: string;
  audioUrl?: string;  // Optionnel si tu veux gérer l'audio
}

interface AskResponse {
  answer: string;
  audio_url?: string;
}

@Component({
  selector: 'app-chat-assistant',
  templateUrl: './chat-assistant.component.html',
  styleUrls: ['./chat-assistant.component.css']
})
export class ChatAssistantComponent {
  messages: ChatMessage[] = [];
  userInput = '';
  loading = false;
  isOpen = false;

  private readonly API_URL = '/ask-assis';

  @ViewChild('chatBody') chatBodyRef?: ElementRef<HTMLDivElement>;

  constructor(private http: HttpClient) {}

  toggleChat(): void {
    this.isOpen = !this.isOpen;
    setTimeout(() => this.scrollToBottom(), 100);
  }

  sendMessage(): void {
    const question = this.userInput.trim();
    if (!question) return;

    this.messages.push({ sender: 'Vous', text: question });
    this.userInput = '';
    this.loading = true;
    setTimeout(() => this.scrollToBottom(), 100);

    const body = new HttpParams().set('question', question);

    this.http.post<AskResponse>(this.API_URL, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .pipe(finalize(() => {
      this.loading = false;
      this.scrollToBottom();
    }))
    .subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.answer, audioUrl: res.audio_url });
        if (res.audio_url) {
          const audio = new Audio(res.audio_url);
          audio.play();
        }
      },
      error: (err: HttpErrorResponse) => {
        let errMsg = 'Erreur inconnue.';
        if (typeof err.error === 'string') errMsg = err.error;
        else if (err.error?.error) errMsg = err.error.error;
        else if (err.statusText) errMsg = err.statusText;
        this.messages.push({ sender: 'Bot', text: `❌ ${errMsg}` });
      }
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.chatBodyRef?.nativeElement) {
        this.chatBodyRef.nativeElement.scrollTo({
          top: this.chatBodyRef.nativeElement.scrollHeight,
          behavior: 'smooth'
        });
      }
    }, 0);
  }
}
