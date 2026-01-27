import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FooterCopyrightComponent } from './footer-copyright.component';

describe('FooterCopyrightComponent', () => {
  let component: FooterCopyrightComponent;
  let fixture: ComponentFixture<FooterCopyrightComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FooterCopyrightComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FooterCopyrightComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
