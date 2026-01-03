import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SideBarItems } from './side-bar-items';

describe('SideBarItems', () => {
  let component: SideBarItems;
  let fixture: ComponentFixture<SideBarItems>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SideBarItems]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SideBarItems);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
