import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ConsortiumService } from '../../../services/consortium.service';
import { ConsortiumStatus } from '../../../../models/consortium.model';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-form',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, LabelComponent],
  templateUrl: './consortium-form.html',
  styleUrl: './consortium-form.css',
  standalone: true
})
export class ConsortiumForm implements OnInit {
  form!: FormGroup;
  isEditMode = false;
  consortiumId?: string;
  statusOptions = Object.values(ConsortiumStatus);

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private consortiumService: ConsortiumService
  ) {
    this.form = this.fb.group({
      cuit: ['', [Validators.required, Validators.pattern(/^\d+$/)]],
      razon_social: ['', Validators.required],
      calle: ['', Validators.required],
      numero: [0, [Validators.required, Validators.min(1)]],
      codigo_postal: ['', Validators.required],
      ciudad: ['', Validators.required],
      interes_por_mora: [0, [Validators.required, Validators.min(0)]],
      redondeo_aumento: [0, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const idParam = params['consortiumId'];
      if (idParam) {
        this.isEditMode = true;
        this.consortiumId = String(idParam);
        this.loadConsortium(this.consortiumId);
      }
    });
  }

  loadConsortium(id: string): void {
    this.consortiumService.getConsortiumDetail(id).subscribe(consortium => {
      if (consortium) {
        this.form.patchValue({
          cuit: consortium.cuit,
          razon_social: consortium.razon_social,
          calle: consortium.calle,
          numero: consortium.numero,
          codigo_postal: consortium.codigo_postal,
          ciudad: consortium.ciudad,
          interes_por_mora: consortium.interes_por_mora,
          redondeo_aumento: consortium.redondeo_aumento
        });
      }
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      Object.keys(this.form.controls).forEach(key => this.form.get(key)?.markAsTouched());
      return;
    }

    const formValue = this.form.value;
    if (this.isEditMode && this.consortiumId) {
      this.consortiumService.updateConsortium(this.consortiumId, formValue).subscribe({
        next: () => this.router.navigate(['/']),
        error: (error: any) => {
          alert('Error al actualizar consorcio.');
          console.error('Error al actualizar consorcio:', error);
        }
      });
      return;
    }

    this.consortiumService.createConsortium(formValue).subscribe({
      next: () => this.router.navigate(['/']),
      error: (error: any) => {
        const message = this.getErrorMessage(error, 'Error al crear consorcio.');
        alert(message);
        console.error('Error al crear consorcio:', error);
      }
    });
  }

  onCancel(): void {
    this.router.navigate(['/']);
  }

  private getErrorMessage(error: any, fallback: string): string {
    const apiMessage = error?.error?.message || error?.message;
    const apiErrors = error?.error?.errors;
    if (apiErrors && typeof apiErrors === 'object') {
      const details = Object.entries(apiErrors)
        .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : String(messages)}`)
        .join(' | ');
      return `${apiMessage || fallback} (${details})`;
    }
    return apiMessage || fallback;
  }
}
