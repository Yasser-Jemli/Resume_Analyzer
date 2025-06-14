import { TestBed } from '@angular/core/testing';

import { ParserServiceService } from './parser-service.service';

describe('ParserServiceService', () => {
  let service: ParserServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ParserServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
