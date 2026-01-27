import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumDashboardCardsComponent } from './consortium-dashboard-cards.component';

describe('ConsortiumDashboardCardsComponent', () => {
  let component: ConsortiumDashboardCardsComponent;
  let fixture: ComponentFixture<ConsortiumDashboardCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumDashboardCardsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumDashboardCardsComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
