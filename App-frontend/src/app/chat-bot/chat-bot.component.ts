import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.css']
})
export class ChatBotComponent implements OnInit, OnDestroy {
  messages: { sender: string; text: string; score?: number }[] = [];
  userInput = '';

  finalScore = 0;
  questionCount = 0;
  readonly MAX_QUESTIONS = 20;

  sessionActive = true;

  readonly TIMEOUT_MS = 30000;
  timeLeft = this.TIMEOUT_MS / 1000;
  private timerId: any;
  private countdownId: any;

  apiAsk      = '/entretien-ask';
  apiPing     = '/ping';
  apiSendMail = '/send-final-score';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.pingBackend();
    this.queryBot('');  // 1ʳᵉ question
  }

  ngOnDestroy(): void {
    this.clearTimers();
  }

  sendMessage(): void {
    if (!this.sessionActive) return;
    const txt = this.userInput.trim();
    if (!txt) return;
    this.messages.push({ sender: 'Vous', text: txt });
    this.userInput = '';
    // L'utilisateur vient de répondre → incrémente le compteur
    this.questionCount++;
    this.queryBot(txt);
  }

  private queryBot(user_input: string): void {
    this.clearTimers();
    this.timeLeft = this.TIMEOUT_MS / 1000;
    if (!this.sessionActive) return;

    this.http.post<{ response: string; finished?: boolean }>(
      this.apiAsk, { user_input }
    ).subscribe({
      next: res => {
        this.messages.push({ sender: 'Bot', text: res.response });

        // Note éventuelle
        const score = this.extractScore(res.response);
        if (score !== undefined) {
          this.finalScore += score;
          this.messages[this.messages.length - 1].score = score;
        }

        // Fin d'entretien demandée par le backend ou max de questions atteint
        const isFinMsg = /Fin de l’entretien/i.test(res.response);
        if (res.finished || isFinMsg || this.questionCount >= this.MAX_QUESTIONS) {
          this.sessionActive = false;
          this.clearTimers();
          this.timeLeft = 0;
          this.sendFinalScoreMail();
          return;
        }

        // Sinon, on lance le compte à rebours et on programme la suite
        this.startCountdown();
        this.scheduleNextQuestion();
      },
      error: err => {
        console.error(err);
        this.messages.push({
          sender: 'Bot',
          text: 'Erreur de communication avec le serveur.'
        });
      }
    });
  }

  private scheduleNextQuestion(): void {
    this.timerId = setTimeout(() => {
      if (!this.sessionActive) return;
      // pas de réponse → incrémente compteur et affiche message
      this.questionCount++;
      this.messages.push({
        sender: 'Bot',
        text: '⏰ Temps écoulé, question suivante…',
        score: 0
      });
      // Si on a dépassé le max, on termine
      if (this.questionCount >= this.MAX_QUESTIONS) {
        this.messages.push({ sender: 'Bot', text: 'Fin de l’entretien. Merci pour votre temps.' });
        this.sessionActive = false;
        this.timeLeft = 0;
        this.sendFinalScoreMail();
      } else {
        this.queryBot('');
      }
    }, this.TIMEOUT_MS);
  }

  private extractScore(text: string): number|undefined {
    if (/Fin de l’entretien/i.test(text)) return undefined;
    const m = text.match(/Note\s*:\s*(\d{1,2})\/20/i);
    return m ? parseInt(m[1], 10) : undefined;
  }

  private startCountdown(): void {
    this.countdownId = setInterval(() => {
      this.timeLeft--;
      if (this.timeLeft <= 0) {
        clearInterval(this.countdownId);
      }
    }, 1000);
  }

  private clearTimers(): void {
    if (this.timerId)    { clearTimeout(this.timerId); this.timerId = null; }
    if (this.countdownId){ clearInterval(this.countdownId); this.countdownId = null; }
  }

  getStars(score: number): string {
    if (score >= 16) return '⭐⭐⭐⭐⭐';
    if (score >= 12) return '⭐⭐⭐⭐';
    if (score >= 8)  return '⭐⭐⭐';
    if (score >= 4)  return '⭐⭐';
    return '⭐';
  }

  private sendFinalScoreMail(): void {
    const payload = {
      finalScore: this.finalScore,
      maxScore:   this.questionCount * 20,
      questions:  this.questionCount
    };
    this.http.post(this.apiSendMail, payload).subscribe();
  }

  private pingBackend(): void {
    this.http.get(this.apiPing, { responseType: 'text' }).subscribe();
  }

  get questionLabel(): string {
    const next = this.questionCount + 1;
    return next <= this.MAX_QUESTIONS
      ? `Question ${next} / ${this.MAX_QUESTIONS}`
      : `Toutes les questions ont été posées`;
  }
}
