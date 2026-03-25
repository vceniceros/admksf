import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumEventsCardComponent } from './consortium-events-card.component';

describe('ConsortiumEventsCardComponent', () => {
  let component: ConsortiumEventsCardComponent;
  let fixture: ComponentFixture<ConsortiumEventsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumEventsCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumEventsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
