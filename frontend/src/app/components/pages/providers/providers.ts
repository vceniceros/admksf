import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { catchError, of, switchMap } from 'rxjs';
import { ProvidersService } from '../../../services/providers.service';
import { ApiErrorService } from '../../../services/api-error.service';
import { Provider } from '../../../../models/provider.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { ProvidersTableComponent } from '../../molecules/providers-table.component/providers-table.component';

@Component({
  selector: 'app-providers',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LabelComponent,
    IconComponent,
    ProvidersTableComponent
  ],
  templateUrl: './providers.html',
  styleUrl: './providers.css',
  standalone: true
})
export class Providers implements OnInit {
  providers: Provider[] = [];
  showFormModal = false;
  showDeleteModal = false;
  isEditMode = false;
  selectedProvider: Provider | null = null;
  providerToDelete: Provider | null = null;
  form: FormGroup;
  originalTipo: string | null = null;

  tipoOptions = [
    { value: 'servicios_mensuales', label: 'Servicio' },
    { value: 'reparaciones_mantenimientos', label: 'Mantenimiento' }
  ];

  constructor(
    private route: ActivatedRoute,
    private providersService: ProvidersService,
    private apiErrorService: ApiErrorService,
    private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      cuit: ['', [Validators.required, Validators.pattern(/^\d+$/)]],
      razon_social: ['', Validators.required],
      telefono: [''],
      email: ['', Validators.email],
      calle: ['', Validators.required],
      numero: ['', [Validators.required, Validators.min(1)]],
      codigo_postal: ['', Validators.required],
      ciudad: ['', Validators.required],
      tipo_proveedor: ['', Validators.required],
      numero_cuenta: [''],
      numero_reclamo: ['']
    });

    this.form.get('tipo_proveedor')?.valueChanges.subscribe(value => {
      this.applyTipoValidators(value);
    });
  }

  ngOnInit() {
    this.route.params.subscribe(() => {
      this.loadProviders();
    });
  }

  loadProviders() {
    this.providersService.getAllProviders().subscribe({
      next: (data) => {
        this.providers = data;
      },
      error: (error) => {
        console.error('Error loading providers:', error);
      }
    });
  }

  openCreateModal() {
    this.isEditMode = false;
    this.selectedProvider = null;
    this.originalTipo = null;
    this.form.reset({
      cuit: '',
      razon_social: '',
      telefono: '',
      email: '',
      calle: '',
      numero: '',
      codigo_postal: '',
      ciudad: '',
      tipo_proveedor: '',
      numero_cuenta: '',
      numero_reclamo: ''
    });
    this.showFormModal = true;
  }

  openEditModal(provider: Provider) {
    this.isEditMode = true;
    this.selectedProvider = provider;
    this.originalTipo = provider.tipo_proveedor;
    this.showFormModal = true;

    this.providersService.getProviderByCuit(provider.cuit).subscribe({
      next: (fullProvider) => {
        if (!fullProvider) {
          return;
        }
        this.form.reset({
          cuit: fullProvider.cuit,
          razon_social: fullProvider.razon_social,
          telefono: fullProvider.telefono ?? '',
          email: fullProvider.email ?? '',
          calle: fullProvider.calle,
          numero: fullProvider.numero,
          codigo_postal: fullProvider.codigo_postal,
          ciudad: fullProvider.ciudad,
          tipo_proveedor: fullProvider.tipo_proveedor,
          numero_cuenta: '',
          numero_reclamo: ''
        });

        if (fullProvider.tipo_proveedor === 'servicios_mensuales') {
          this.providersService.getServicioMensual(fullProvider.cuit).subscribe({
            next: (detalle) => {
              this.form.patchValue({
                numero_cuenta: detalle?.numero_cuenta ?? '',
                numero_reclamo: detalle?.numero_reclamo ?? ''
              });
            }
          });
        } else if (fullProvider.tipo_proveedor === 'reparaciones_mantenimientos') {
          this.providersService.getReparacionMantenimiento(fullProvider.cuit).subscribe({
            next: (detalle) => {
              this.form.patchValue({
                numero_reclamo: detalle?.numero_reclamo ?? ''
              });
            }
          });
        }
      },
      error: (error) => {
        console.error('Error loading provider detail:', error);
      }
    });
  }

  closeFormModal() {
    this.showFormModal = false;
  }

  submitForm() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const raw = this.form.getRawValue();
    const cuit = String(raw.cuit ?? '').trim();
    const basePayload = {
      cuit,
      razon_social: raw.razon_social,
      telefono: raw.telefono || null,
      email: raw.email || null,
      calle: raw.calle,
      numero: Number(raw.numero),
      codigo_postal: raw.codigo_postal,
      ciudad: raw.ciudad,
      tipo_proveedor: raw.tipo_proveedor
    };

    const tipo = raw.tipo_proveedor;

    if (this.isEditMode && this.selectedProvider) {
      this.providersService.updateProvider(this.selectedProvider.cuit, basePayload).subscribe({
        next: () => {
          this.syncSpecialization(cuit, tipo, this.originalTipo);
        },
        error: (error) => {
          const message = this.apiErrorService.extractDetailedMessage(error, 'Error al actualizar proveedor.');
          alert(message);
          console.error('Error updating provider:', error);
        }
      });
      return;
    }

    this.providersService.createProvider(basePayload).subscribe({
      next: () => {
        this.createSpecialization(cuit, tipo, raw);
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al crear proveedor.');
        alert(message);
        console.error('Error creating provider:', error);
      }
    });
  }

  private createSpecialization(cuit: string, tipo: string, raw: any) {
    if (tipo === 'servicios_mensuales') {
      this.providersService.createServicioMensual({
        proveedor: cuit,
        numero_cuenta: raw.numero_cuenta,
        numero_reclamo: raw.numero_reclamo
      }).subscribe({
        next: () => {
          this.closeFormModal();
          this.loadProviders();
        },
        error: (error) => {
          const message = this.apiErrorService.extractDetailedMessage(error, 'Error al crear servicio mensual.');
          alert(message);
          console.error('Error creating servicio mensual:', error);
        }
      });
      return;
    }

    this.providersService.createReparacionMantenimiento({
      proveedor: cuit,
      numero_reclamo: raw.numero_reclamo
    }).subscribe({
      next: () => {
        this.closeFormModal();
        this.loadProviders();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al crear mantenimiento.');
        alert(message);
        console.error('Error creating mantenimiento:', error);
      }
    });
  }

  private syncSpecialization(cuit: string, tipo: string, originalTipo: string | null) {
    if (originalTipo && originalTipo !== tipo) {
      const delete$ = originalTipo === 'servicios_mensuales'
        ? this.providersService.deleteServicioMensual(cuit)
        : this.providersService.deleteReparacionMantenimiento(cuit);

      delete$.subscribe({
        next: () => this.createSpecialization(cuit, tipo, this.form.getRawValue()),
        error: () => this.createSpecialization(cuit, tipo, this.form.getRawValue())
      });
      return;
    }

    if (tipo === 'servicios_mensuales') {
      const payload = {
        proveedor: cuit,
        numero_cuenta: this.form.get('numero_cuenta')?.value,
        numero_reclamo: this.form.get('numero_reclamo')?.value
      };
      this.providersService.updateServicioMensual(cuit, payload).pipe(
        catchError(() => this.providersService.createServicioMensual(payload)),
        switchMap(() => of(true))
      ).subscribe({
        next: () => {
          this.closeFormModal();
          this.loadProviders();
        },
        error: (error) => {
          const message = this.apiErrorService.extractDetailedMessage(error, 'Error al actualizar servicio mensual.');
          alert(message);
          console.error('Error updating servicio mensual:', error);
        }
      });
      return;
    }

    const payload = {
      proveedor: cuit,
      numero_reclamo: this.form.get('numero_reclamo')?.value
    };
    this.providersService.updateReparacionMantenimiento(cuit, payload).pipe(
      catchError(() => this.providersService.createReparacionMantenimiento(payload)),
      switchMap(() => of(true))
    ).subscribe({
      next: () => {
        this.closeFormModal();
        this.loadProviders();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al actualizar mantenimiento.');
        alert(message);
        console.error('Error updating mantenimiento:', error);
      }
    });
  }

  applyTipoValidators(tipo: string) {
    const cuenta = this.form.get('numero_cuenta');
    const reclamo = this.form.get('numero_reclamo');

    cuenta?.clearValidators();
    reclamo?.clearValidators();

    if (tipo === 'servicios_mensuales') {
      cuenta?.setValidators([Validators.required]);
      reclamo?.setValidators([Validators.required]);
    } else if (tipo === 'reparaciones_mantenimientos') {
      reclamo?.setValidators([Validators.required]);
      cuenta?.setValue('');
    }

    cuenta?.updateValueAndValidity();
    reclamo?.updateValueAndValidity();
  }

  onDeleteProvider(provider: Provider) {
    this.providerToDelete = provider;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.providerToDelete = null;
  }

  confirmDelete() {
    if (!this.providerToDelete) {
      return;
    }
    this.providersService.deleteProvider(this.providerToDelete.cuit).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.loadProviders();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al eliminar proveedor.');
        alert(message);
        console.error('Error deleting provider:', error);
      }
    });
  }
}
