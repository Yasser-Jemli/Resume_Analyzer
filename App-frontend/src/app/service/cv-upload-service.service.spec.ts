import { TestBed } from '@angular/core/testing';

import { CvUploadServiceService } from './cv-upload-service.service';

describe('CvUploadServiceService', () => {
  let service: CvUploadServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CvUploadServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
