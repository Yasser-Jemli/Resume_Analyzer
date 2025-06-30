import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ChatInterviewServiceService {

  private apiUrl = 'http://172.0.0.196:5003'; // URL de l'API pour les interviews

  // Subject pour partager les skills sélectionnées avec le chatbot
  private skillsSubject = new BehaviorSubject<string[] | null>(null);
  skills$ = this.skillsSubject.asObservable();

  constructor(private http: HttpClient) { }

  // Setter pour envoyer les skills au chatbot (en mémoire + backend)
  setSkills(skills: string[]) {
    this.skillsSubject.next(skills);
    // Mettre à jour les skills dans le backend (json-server)
    this.http.patch<{skills: string[]}>(this.apiUrl, { skills }).subscribe();
  }

  // Getter pour récupérer les skills dans le chatbot (mémoire)
  getSkills(): Observable<string[] | null> {
    return this.skills$;
  }

  // Récupérer les skills depuis le backend (optionnel)
  fetchSkillsFromBackend(): Observable<{skills: string[]}> {
    return this.http.get<{skills: string[]}>(this.apiUrl);
  }
  sendposttochatbot(post: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/sendPost`, post);
  }
}
