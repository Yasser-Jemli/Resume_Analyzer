import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { finalize } from 'rxjs/operators';

interface ChatMessage {
  sender: 'Vous' | 'Bot';
  text: string;
}

interface AskResponse {
  answer: string;
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

  /** URL du backend (centralisé) */
  private readonly API_URL = '/askquest';

  @ViewChild('chatBody') chatBodyRef?: ElementRef<HTMLDivElement>;

  constructor(private http: HttpClient) {}

  toggleChat(): void {
    this.isOpen = !this.isOpen;
    this.scrollToBottom();
  }

  sendMessage(): void {
    const question = this.userInput.trim();
    if (!question) {
      return;
    }

    // Ajoute le message utilisateur
    this.messages.push({ sender: 'Vous', text: question });
    this.userInput = '';
    this.loading = true;
    this.scrollToBottom();

    // Prépare le corps en x-www-form-urlencoded
    const body = new HttpParams().set('question', question);

    console.log('Envoi question à:', this.API_URL, 'avec body:', body.toString());

    this.http.post<AskResponse>(this.API_URL, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .pipe(finalize(() => {
      this.loading = false;
      this.scrollToBottom();
    }))
    .subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.answer });
      },
      error: (err: HttpErrorResponse) => {
        let errMsg = 'Erreur inconnue.';
        if (typeof err.error === 'string') {
          errMsg = err.error;
        } else if (err.error?.error) {
          errMsg = err.error.error;
        } else if (err.statusText) {
          errMsg = err.statusText;
        }
        this.messages.push({ sender: 'Bot', text: `❌ ${errMsg}` });
      }
    });
  }

  /** Fait défiler la fenêtre de chat vers le bas */
  private scrollToBottom(): void {
    setTimeout(() => {
      this.chatBodyRef?.nativeElement.scrollTo({
        top: this.chatBodyRef.nativeElement.scrollHeight,
        behavior: 'smooth'
      });
    }, 0);
  }
}

