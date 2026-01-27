import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumLastPaymentCardFoundCardComponent } from './consortium-last-payment-card-found-card.component';

describe('ConsortiumLastPaymentCardFoundCardComponent', () => {
  let component: ConsortiumLastPaymentCardFoundCardComponent;
  let fixture: ComponentFixture<ConsortiumLastPaymentCardFoundCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumLastPaymentCardFoundCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumLastPaymentCardFoundCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
