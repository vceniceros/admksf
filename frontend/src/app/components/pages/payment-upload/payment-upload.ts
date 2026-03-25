import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PaymentService } from '../../../services/payment.services';
import { ConsortiumService } from '../../../services/consortium.service';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-payment-upload',
  imports: [CommonModule, ReactiveFormsModule, LabelComponent],
  templateUrl: './payment-upload.html',
  styleUrl: './payment-upload.css',
  standalone: true
})
export class PaymentUpload implements OnInit {
  paymentForm!: FormGroup;
  consortiumName: string = '';
  consortiumId: string = '';
  statusOptions = ['Aprobado', 'Pendiente', 'Parcial'];
  isEditMode = false;
  paymentId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private paymentService: PaymentService,
    private consortiumService: ConsortiumService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.paymentForm = this.fb.group({
      cuitConsorcio: ['', Validators.required],
      numeroUnidad: ['', [Validators.required, Validators.min(1)]],
      dniPropietario: ['', [Validators.required, Validators.pattern(/^\d+$/)]],
      monto: [0, [Validators.required, Validators.min(0.01)]],
      estadoPago: ['Pendiente', Validators.required],
      fechaPago: ['']
    });
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      const idParam = params['idPago'];
      this.paymentId = idParam ? Number(idParam) : null;
      this.isEditMode = !!this.paymentId;
      this.loadConsortiumData();
    });
  }

  loadConsortiumData() {
    this.consortiumService.getAllConsortiums().subscribe({
      next: (consortia) => {
        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
        if (found) {
          this.consortiumId = String(found.id);
          this.paymentForm.patchValue({ cuitConsorcio: this.consortiumId });
          if (this.isEditMode && this.paymentId) {
            this.loadPayment();
          }
        }
      },
      error: (error) => {
        console.error('Error loading consortium:', error);
      }
    });
  }

  loadPayment() {
    if (!this.paymentId) {
      return;
    }
    this.paymentService.getPaymentById(this.paymentId).subscribe({
      next: (payment) => {
        if (!payment) {
          return;
        }
        this.paymentForm.patchValue({
          cuitConsorcio: payment.cuitConsorcio ?? this.consortiumId,
          numeroUnidad: payment.numeroUnidad ?? '',
          dniPropietario: payment.propietario ?? '',
          monto: payment.amount,
          estadoPago: payment.status,
          fechaPago: payment.fechaPago ?? ''
        });
      },
      error: (error) => {
        console.error('Error loading payment:', error);
      }
    });
  }

  onSubmit() {
    if (this.paymentForm.invalid) {
      this.paymentForm.markAllAsTouched();
      return;
    }

    const formValue = this.paymentForm.value;
    const payload = {
      numero_de_unidad_funcional: Number(formValue.numeroUnidad),
      consorcio: formValue.cuitConsorcio,
      propietario: String(formValue.dniPropietario ?? '').trim(),
      monto: formValue.monto,
      estado_pago: formValue.estadoPago,
      fecha_pago: formValue.fechaPago || undefined
    };

    if (this.isEditMode && this.paymentId) {
      this.paymentService.updatePayment(this.paymentId, payload).subscribe({
        next: () => {
          this.router.navigate(['/dashboard', this.consortiumName, 'pagos']);
        },
        error: (error: any) => {
          console.error('Error al actualizar pago:', error);
        }
      });
      return;
    }

    this.paymentService.createPayment(payload).subscribe({
      next: () => {
        this.router.navigate(['/dashboard', this.consortiumName, 'pagos']);
      },
      error: (error: any) => {
        console.error('Error al agregar pago:', error);
      }
    });
  }

  onCancel() {
    this.router.navigate(['/dashboard', this.consortiumName, 'pagos']);
  }
}
