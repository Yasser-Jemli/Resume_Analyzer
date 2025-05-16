import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestMonCvComponent } from './test-mon-cv.component';

describe('TestMonCvComponent', () => {
  let component: TestMonCvComponent;
  let fixture: ComponentFixture<TestMonCvComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TestMonCvComponent]
    });
    fixture = TestBed.createComponent(TestMonCvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
