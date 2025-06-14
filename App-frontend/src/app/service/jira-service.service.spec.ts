import { TestBed } from '@angular/core/testing';

import { JiraServiceService } from './jira-service.service';

describe('JiraServiceService', () => {
  let service: JiraServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JiraServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
