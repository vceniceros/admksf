import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpendingTableComponent } from './spending-table.component';

describe('SpendingTableComponent', () => {
  let component: SpendingTableComponent;
  let fixture: ComponentFixture<SpendingTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpendingTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpendingTableComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
