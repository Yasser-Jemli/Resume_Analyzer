import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ParserServiceService {

  private apiUrl = 'http://localhost:8081/scores';

  constructor(private http: HttpClient) { }

  // Service pour récupérer les scores (utilisé dans getMyNote)
  getScores(): Observable<any> {
    return this.http.get<any>('http://localhost:8081/scores');
  }
  getLearningPath(): Observable<any> {
    return this.http.get<any>('http://localhost:8081/learning_path');
  }
  getSkillRecommendations(): Observable<any> {
    return this.http.get<any>('http://localhost:8081/skill_recommendations');
  }
}
