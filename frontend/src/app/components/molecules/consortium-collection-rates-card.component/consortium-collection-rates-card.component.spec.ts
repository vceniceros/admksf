import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumCollectionRatesCardComponent } from './consortium-collection-rates-card.component';

describe('ConsortiumCollectionRatesCardComponent', () => {
  let component: ConsortiumCollectionRatesCardComponent;
  let fixture: ComponentFixture<ConsortiumCollectionRatesCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumCollectionRatesCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumCollectionRatesCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
