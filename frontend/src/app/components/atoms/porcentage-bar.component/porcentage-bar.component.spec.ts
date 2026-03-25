import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PorcentageBarComponent } from './porcentage-bar.component';

describe('PorcentageBarComponent', () => {
  let component: PorcentageBarComponent;
  let fixture: ComponentFixture<PorcentageBarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PorcentageBarComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PorcentageBarComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
