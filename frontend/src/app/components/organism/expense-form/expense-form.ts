import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup } from '@angular/forms';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { TipoGasto, EstadoPago } from '../../../../models/spends.model';

@Component({
  selector: 'app-expense-form',
  imports: [CommonModule, ReactiveFormsModule, LabelComponent],
  templateUrl: './expense-form.html',
  styleUrl: './expense-form.css',
  standalone: true
})
export class ExpenseForm {
  @Input() form!: FormGroup;
  
  TipoGasto = TipoGasto;
  EstadoPago = EstadoPago;
  
  tipoGastoOptions = Object.values(TipoGasto);
  estadoPagoOptions = Object.values(EstadoPago);
  
  get periodo() { return this.form.get('periodo'); }
  get tipoGasto() { return this.form.get('tipoGasto'); }
  get descripcion() { return this.form.get('descripcion'); }
  get cuitProveedor() { return this.form.get('cuitProveedor'); }
  get monto() { return this.form.get('monto'); }
  get estadoPago() { return this.form.get('estadoPago'); }
  get cuitConsorcio() { return this.form.get('cuitConsorcio'); }
}