import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumMenuComponent } from './consortium-menu.component';

describe('ConsortiumMenuComponent', () => {
  let component: ConsortiumMenuComponent;
  let fixture: ComponentFixture<ConsortiumMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumMenuComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumMenuComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
