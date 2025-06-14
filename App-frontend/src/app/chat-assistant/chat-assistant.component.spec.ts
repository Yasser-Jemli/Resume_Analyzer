import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatAssistantComponent } from './chat-assistant.component';

describe('ChatAssistantComponent', () => {
  let component: ChatAssistantComponent;
  let fixture: ComponentFixture<ChatAssistantComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ChatAssistantComponent]
    });
    fixture = TestBed.createComponent(ChatAssistantComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
