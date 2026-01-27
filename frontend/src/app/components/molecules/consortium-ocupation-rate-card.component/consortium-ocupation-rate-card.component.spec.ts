import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumOcupationRateCardComponent } from './consortium-ocupation-rate-card.component';

describe('ConsortiumOcupationRateCardComponent', () => {
  let component: ConsortiumOcupationRateCardComponent;
  let fixture: ComponentFixture<ConsortiumOcupationRateCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumOcupationRateCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumOcupationRateCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
