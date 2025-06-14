import { TestBed } from '@angular/core/testing';

import { ChatInterviewServiceService } from './chat-interview-service.service';

describe('ChatInterviewServiceService', () => {
  let service: ChatInterviewServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ChatInterviewServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
