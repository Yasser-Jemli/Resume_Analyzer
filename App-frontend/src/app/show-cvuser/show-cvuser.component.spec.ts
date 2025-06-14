import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowCvuserComponent } from './show-cvuser.component';

describe('ShowCvuserComponent', () => {
  let component: ShowCvuserComponent;
  let fixture: ComponentFixture<ShowCvuserComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShowCvuserComponent]
    });
    fixture = TestBed.createComponent(ShowCvuserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
