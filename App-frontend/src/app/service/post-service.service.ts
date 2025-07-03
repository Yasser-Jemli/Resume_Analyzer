import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Post } from '../models/post.model';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private apiUrl = 'http://localhost:8081/posts';

  constructor(private http: HttpClient) {}

  /**
   * Retrieves all posts from the backend.
   * @returns Observable<Post[]> containing the list of posts.
   */
  getPosts(): Observable<Post[]> {
    return this.http.get<Post[]>(`${this.apiUrl}/getAllPosts`).pipe(
      catchError(this.handleError('fetch posts'))
    );
  }

  /**
   * Retrieves posts for a specific user by their ID.
   * @param userId The ID of the user.
   * @returns Observable<Post[]> containing the user's posts.
   */
  getPostsByManager(userId: number): Observable<Post[]> {
  return this.http.get<Post[]>(`${this.apiUrl}/manager/${userId}`);
}


  /**
   * Creates a new post for the given user.
   * @param userId The ID of the user creating the post.
   * @param post The post data to create.
   * @returns Observable<Post> containing the created post.
   */
  createPost(userId: number, post: Post): Observable<Post> {
  return this.http.post<Post>(`${this.apiUrl}/createPost/${userId}`, post).pipe(
    catchError(this.handleError('create post'))
  );
  }


  /**
   * Updates an existing post.
   * @param id The ID of the post to update.
   * @param post The updated post data.
   * @returns Observable<Post> containing the updated post.
   */
  updatePost(id: number, post: Post): Observable<Post> {
    return this.http.put<Post>(`${this.apiUrl}/update/${id}`, post).pipe(
      catchError(this.handleError('update post'))
    );
  }

  /**
   * Deletes a post by its ID.
   * @param id The ID of the post to delete.
   * @returns Observable<void> indicating success.
   */
  deletePost(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/deletPost/${id}`).pipe(
      catchError(this.handleError('delete post'))
    );
  }

  /**
   * Handles HTTP errors and provides meaningful messages.
   * @param operation The operation that failed.
   * @returns Error handler function.
   */
  private handleError(operation: string) {
    return (error: HttpErrorResponse): Observable<never> => {
      let errorMsg = `Error during ${operation}`;
      if (error.error instanceof ErrorEvent) {
        errorMsg = `Client-side error: ${error.error.message}`;
      } else if (error.status === 0) {
        errorMsg = 'Network error: Unable to reach the server';
      } else {
        errorMsg = `Server error: ${error.status} - ${error.error?.error || error.statusText || 'Unknown error'}`;
        if (error.status === 400 && error.error?.error.includes('JSON')) {
          errorMsg = 'Invalid JSON response from server';
        }
      }
      console.error(errorMsg, error);
      return throwError(() => new Error(errorMsg));
    };
  }
}