import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommonSpendesGridComponent } from './common-spendes-grid.component';

describe('CommonSpendesGridComponent', () => {
  let component: CommonSpendesGridComponent;
  let fixture: ComponentFixture<CommonSpendesGridComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommonSpendesGridComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommonSpendesGridComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
