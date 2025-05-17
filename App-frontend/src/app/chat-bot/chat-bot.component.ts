import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.css']
})
export class ChatBotComponent implements OnInit {
  messages: { sender: string; text: string }[] = [];
  userInput: string = '';

  // URL du backend Flask (via proxy si configuré)
  apiAsk: string = '/entretien-ask';
  apiPing: string = '/ping';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.testBackend(); // appel initial pour tester le backend
  }

  sendMessage(): void {
    const trimmedInput = this.userInput.trim();
    if (!trimmedInput) return;

    this.messages.push({ sender: 'Vous', text: trimmedInput });

    this.http.post<{ response: string }>(this.apiAsk, { user_input: trimmedInput }).subscribe({
      next: (res) => {
        this.messages.push({ sender: 'Bot', text: res.response });
        this.userInput = '';
      },
      error: (err) => {
        console.error('Erreur backend:', err);
        this.messages.push({ sender: 'Bot', text: 'Erreur lors de la communication avec le serveur.' });
      }
    });
  }

  testBackend(): void {
    this.http.get(this.apiPing, { responseType: 'text' }).subscribe({
      next: (res) => {
        console.log('Backend accessible:', res); // doit afficher "pong"
      },
      error: (err) => {
        console.error('Erreur connexion backend:', err);
      }
    });
  }
}
