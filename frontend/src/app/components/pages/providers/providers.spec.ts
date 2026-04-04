import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';
import { Providers } from './providers';
import { ProvidersService } from '../../../services/providers.service';
import { ApiErrorService } from '../../../services/api-error.service';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

describe('Providers Form Validation', () => {
  let component: Providers;
  let fixture: ComponentFixture<Providers>;
  let mockProvidersService: any;
  let mockApiErrorService: any;
  let mockActivatedRoute: any;

  beforeEach(async () => {
    mockProvidersService = {
      getAllProviders: jasmine.createSpy().and.returnValue(of([])),
      getProviderByCuit: jasmine.createSpy(),
      createProvider: jasmine.createSpy(),
      updateProvider: jasmine.createSpy(),
      deleteProvider: jasmine.createSpy()
    };

    mockApiErrorService = {
      extractDetailedMessage: jasmine.createSpy().and.returnValue('Generic error')
    };

    mockActivatedRoute = {
      params: of({})
    };

    await TestBed.configureTestingModule({
      imports: [Providers, ReactiveFormsModule],
      providers: [
        { provide: ProvidersService, useValue: mockProvidersService },
        { provide: ApiErrorService, useValue: mockApiErrorService },
        { provide: ActivatedRoute, useValue: mockActivatedRoute }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(Providers);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should mark form as invalid when empty', () => {
    component.openCreateModal();
    fixture.detectChanges();
    expect(component.form.invalid).toBeTrue();
  });

  it('should show error messages and red border when required fields are touched and empty', () => {
    component.openCreateModal();
    fixture.detectChanges();

    const cuitControl = component.form.get('cuit');
    cuitControl?.markAsTouched();
    fixture.detectChanges();

    const cuitInput = fixture.debugElement.query(By.css('input[formControlName="cuit"]')).nativeElement;
    const errorMsg = fixture.debugElement.query(By.css('span.error-msg'));

    expect(cuitInput.classList.contains('invalid-input')).toBeTrue();
    expect(errorMsg).toBeTruthy();
    expect(errorMsg.nativeElement.textContent).toContain('Este campo es requerido');
  });

  it('should disable submit button when form is invalid', () => {
    component.openCreateModal();
    fixture.detectChanges();

    const submitBtn = fixture.debugElement.query(By.css('.submit-button')).nativeElement;
    expect(submitBtn.disabled).toBeTrue();
  });

  it('should enable submit button when required fields are filled', () => {
    component.openCreateModal();
    fixture.detectChanges();

    component.form.patchValue({
      cuit: '20123456789',
      razon_social: 'Test SA',
      calle: 'Av Test',
      numero: 123,
      codigo_postal: '1000',
      ciudad: 'CABA',
      tipo_proveedor: 'reparaciones_mantenimientos',
      numero_reclamo: '123456'
    });
    fixture.detectChanges();

    const submitBtn = fixture.debugElement.query(By.css('.submit-button')).nativeElement;
    expect(submitBtn.disabled).toBeFalse();
  });
});
