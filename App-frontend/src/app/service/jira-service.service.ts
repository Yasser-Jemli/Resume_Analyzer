import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class JiraServiceService {
  private skillsSubject = new BehaviorSubject<string[]>([]);
  skills$ = this.skillsSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Appel API pour récupérer les issues
  getIssues(): Observable<any[]> {
    return this.http.get<any[]>('http://localhost:8081/issues');
  }

  // Getter pour récupérer les skills sélectionnées (optionnel)
  getSkills(): Observable<string[]> {
    return this.skills$;
  }
}
