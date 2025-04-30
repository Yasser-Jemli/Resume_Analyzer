import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeadrsComponent } from './headrs.component';

describe('HeadrsComponent', () => {
  let component: HeadrsComponent;
  let fixture: ComponentFixture<HeadrsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HeadrsComponent]
    });
    fixture = TestBed.createComponent(HeadrsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
