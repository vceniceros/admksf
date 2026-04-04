import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { BehaviorSubject, Observable, map, shareReplay } from 'rxjs';

import { ConsortiumService } from '../../../services/consortium.service';
import { SettlementService } from '../../../services/settlement.service';
import {
  SettlementResponse,
  SettlementTableRow,
  SettlementTableState,
  SettlementTemplate
} from '../../../../models/settlement.model';
import { SettlementValuePipe } from '../../../shared/pipes/settlement-value.pipe';
import { ToastComponent } from '../../../shared/components/toast/toast.component';

@Component({
  selector: 'app-settlement',
  imports: [CommonModule, FormsModule, SettlementValuePipe, ToastComponent],
  templateUrl: './settlement.html',
  styleUrl: './settlement.css',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.Default
})
export class SettlementComponent implements OnInit {
  consortiumName: string = '';
  consortiumId: string = '';

  period: string = this.defaultPeriod();
  selectedTemplateId: string = '';

  templates$!: Observable<SettlementTemplate[]>;
  templates: SettlementTemplate[] = [];

  private settlementSubject = new BehaviorSubject<SettlementResponse | null>(null);
  settlement$ = this.settlementSubject.asObservable().pipe(
    map(response => (response ? this.mapToTableState(response) : null)),
    shareReplay(1)
  );

  isPreviewLoading = false;
  isClosing = false;
  showTemplateForm = false;
  isSettlementClosed = false;

  toastMessage = '';
  toastType: 'success' | 'error' = 'success';
  showToast = false;
  isEditTemplate = false;
  showDeleteConfirm = false;
  templateToDelete: SettlementTemplate | null = null;
  formError = '';
  columnError = '';
  templateForm = {
    id: 0,
    nombre: '',
    version: 1,
    activo: true,
    roundingMetodo: 'none',
    roundingIncrement: '0.50',
    columns: [] as any[]
  };
  columnDraft = this.createEmptyColumn();
  editingColumnIndex: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private consortiumService: ConsortiumService,
    private settlementService: SettlementService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      this.loadConsortiumData();
    });
  }

  loadConsortiumData(): void {
    this.consortiumService.getAllConsortiums().subscribe({
      next: (consortia) => {
        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
        if (found) {
          this.consortiumId = String(found.id);
          this.templates$ = this.settlementService.getTemplatesByConsortium(this.consortiumId);
          this.templates$.subscribe({
            next: (items) => {
              this.templates = items;
            }
          });
        }
      }
    });
  }

  preview(): void {
    if (!this.canSubmit()) {
      return;
    }
    this.isPreviewLoading = true;
    const payload = this.buildPayload(false);
    this.settlementService.preview(payload).subscribe({
      next: (response) => {
        this.isSettlementClosed = response.cerrada ?? false;
        this.settlementSubject.next(response);
        this.isPreviewLoading = false;
      },
      error: () => {
        this.isPreviewLoading = false;
      }
    });
  }

  closeSettlement(): void {
    if (!this.canSubmit()) {
      return;
    }
    this.isClosing = true;
    const payload = this.buildPayload(true);
    this.settlementService.closeSettlement(payload).subscribe({
      next: (response) => {
        this.settlementSubject.next({ ...response, cerrada: true });
        this.isSettlementClosed = true;
        this.isClosing = false;
        this.showToastMessage('Liquidación cerrada correctamente', 'success', 4000);
      },
      error: () => {
        this.isClosing = false;
        this.showToastMessage('Error al cerrar la liquidación. Intente nuevamente.', 'error', 6000);
      }
    });
  }

  showToastMessage(message: string, type: 'success' | 'error', duration: number): void {
    this.toastMessage = message;
    this.toastType = type;
    this.showToast = true;
    setTimeout(() => {
      this.showToast = false;
    }, duration);
  }

  openTemplateForm(template?: SettlementTemplate): void {
    if (template) {
      this.isEditTemplate = true;
      this.formError = '';
      this.columnError = '';
      this.templateForm = {
        id: template.id,
        nombre: template.nombre,
        version: template.version,
        activo: template.activo,
        roundingMetodo: 'none',
        roundingIncrement: '0.50',
        columns: []
      };
      this.settlementService.getTemplateById(template.id).subscribe({
        next: (data) => {
          if (data && data.config) {
            const rounding = data.config.rounding ?? {};
            this.templateForm.roundingMetodo = rounding.metodo ?? 'none';
            this.templateForm.roundingIncrement = String(rounding.increment ?? '0.50');
            this.templateForm.columns = Array.isArray(data.config.columns)
              ? data.config.columns
              : [];
          }
        }
      });
    } else {
      this.isEditTemplate = false;
      this.formError = '';
      this.columnError = '';
      this.templateForm = {
        id: 0,
        nombre: '',
        version: 1,
        activo: true,
        roundingMetodo: 'none',
        roundingIncrement: '0.50',
        columns: []
      };
    }
    this.columnDraft = this.createEmptyColumn();
    this.editingColumnIndex = null;
    this.showTemplateForm = true;
  }

  closeTemplateForm(): void {
    this.showTemplateForm = false;
  }

  saveTemplate(): void {
    this.formError = '';
    if (!this.consortiumId) {
      return;
    }
    if (!this.templateForm.nombre || !this.templateForm.nombre.trim()) {
      this.formError = 'El nombre del template es obligatorio.';
      window.alert(this.formError);
      return;
    }
    const formulaIssues = this.validateAllFormulas(this.templateForm.columns);
    if (formulaIssues.length) {
      this.formError = `Fórmula inválida: faltan las columnas ${formulaIssues.join(', ')}.`;
      window.alert(this.formError);
      return;
    }
    const config = {
      rounding: {
        metodo: this.templateForm.roundingMetodo,
        increment: this.templateForm.roundingIncrement
      },
      columns: this.templateForm.columns
    };

    const payload = {
      consorcio: this.consortiumId,
      nombre: this.templateForm.nombre,
      version: Number(this.templateForm.version || 1),
      activo: this.templateForm.activo,
      config
    };

    const request$ = this.isEditTemplate
      ? this.settlementService.updateTemplate(this.templateForm.id, payload)
      : this.settlementService.createTemplate(payload);

    request$.subscribe({
      next: () => {
        this.templates$ = this.settlementService.getTemplatesByConsortium(this.consortiumId);
        this.templates$.subscribe({
          next: (items) => (this.templates = items)
        });
        this.closeTemplateForm();
      }
    });
  }

  deleteTemplate(template: SettlementTemplate): void {
    this.templateToDelete = template;
    this.showDeleteConfirm = true;
  }

  cancelDeleteTemplate(): void {
    this.showDeleteConfirm = false;
    this.templateToDelete = null;
  }

  confirmDeleteTemplate(): void {
    if (!this.templateToDelete) {
      return;
    }
    this.settlementService.deleteTemplate(this.templateToDelete.id).subscribe({
      next: () => {
        this.templates$ = this.settlementService.getTemplatesByConsortium(this.consortiumId);
        this.templates$.subscribe({
          next: (items) => (this.templates = items)
        });
        this.cancelDeleteTemplate();
      }
    });
  }

  addOrUpdateColumn(): void {
    this.columnError = '';
    if (!this.columnDraft.label || !this.columnDraft.calc_type) {
      return;
    }
    const normalized = {
      ...this.columnDraft,
      id: this.normalizeColumnId(this.columnDraft.label)
    };
    if (!normalized.id) {
      return;
    }
    if (normalized.calc_type === 'formula') {
      if (!normalized.expr || !String(normalized.expr).trim()) {
        this.columnError = 'La fórmula es obligatoria.';
        window.alert(this.columnError);
        return;
      }
      const existingIds = this.templateForm.columns
        .map(col => col.id)
        .filter((id: string | undefined) => Boolean(id)) as string[];
      const missing = this.findMissingFormulaIds(String(normalized.expr), existingIds, normalized.id);
      if (missing.length) {
        this.columnError = `Fórmula inválida: faltan las columnas ${missing.join(', ')}.`;
        window.alert(this.columnError);
        return;
      }
    }
    if (this.editingColumnIndex !== null) {
      this.templateForm.columns[this.editingColumnIndex] = normalized;
    } else {
      this.templateForm.columns = [...this.templateForm.columns, normalized];
    }
    this.columnDraft = this.createEmptyColumn();
    this.editingColumnIndex = null;
  }

  editColumn(index: number): void {
    const current = this.templateForm.columns[index];
    if (!current) {
      return;
    }
    this.columnError = '';
    this.columnDraft = { ...current };
    this.editingColumnIndex = index;
  }

  removeColumn(index: number): void {
    this.templateForm.columns = this.templateForm.columns.filter((_, i) => i !== index);
    if (this.editingColumnIndex === index) {
      this.columnDraft = this.createEmptyColumn();
      this.editingColumnIndex = null;
    }
  }

  resetColumnForm(): void {
    this.columnDraft = this.createEmptyColumn();
    this.editingColumnIndex = null;
    this.columnError = '';
  }

  private createEmptyColumn(): any {
    return {
      id: '',
      label: '',
      help_text: '',
      calc_type: '',
      visible: true,
      apply_rounding: false,
      gasto_tipo: '',
      coeficiente: 'superficie',
      metodo: 'simple',
      base: 'saldo_anterior',
      tasa: 'consorcio.interes_por_mora',
      periodos: 1,
      valor: '',
      expr: ''
    };
  }

  private normalizeColumnId(label: string): string {
    return (label || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim()
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[^a-z0-9_]/g, '')
      .replace(/^_+|_+$/g, '');
  }

  private findMissingFormulaIds(expression: string, existingIds: string[], currentId: string): string[] {
    const allowed = new Set(['coeficiente', 'coeficiente_superficie', 'saldo_anterior']);
    const tokens = expression.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) || [];
    const unique = Array.from(new Set(tokens));
    const existing = new Set([...existingIds, currentId, ...allowed]);
    return unique.filter(token => !existing.has(token));
  }

  private validateAllFormulas(columns: any[]): string[] {
    const existingIds = columns.map(col => col.id).filter(Boolean) as string[];
    const missing = new Set<string>();
    columns.forEach(col => {
      if (col.calc_type === 'formula' && col.expr) {
        this.findMissingFormulaIds(String(col.expr), existingIds, col.id || '').forEach(id => missing.add(id));
      }
    });
    return Array.from(missing);
  }

  private canSubmit(): boolean {
    return Boolean(this.consortiumId && this.period && this.selectedTemplateId);
  }

  private buildPayload(cerrar: boolean): any {
    return {
      template_id: Number(this.selectedTemplateId),
      consorcio: this.consortiumId,
      periodo: this.period,
      cerrar
    };
  }

  private mapToTableState(response: SettlementResponse): SettlementTableState {
    const columns = (response.columns || []).filter(col => col.visible !== false);
    const rows: SettlementTableRow[] = (response.unidades || []).map((unidad) => {
      const baseRow: SettlementTableRow = {
        unidad_funcional: String(unidad.numero_unidad_funcional),
        propietario: unidad.propietario,
        apellido: unidad.apellido
      };
      columns.forEach(col => {
        baseRow[col.id] = unidad.valores?.[col.id] ?? '0';
      });
      return baseRow;
    });

    return {
      columns,
      rows,
      totales: response.totales || {},
      templateId: response.template_id,
      periodo: response.periodo,
      cerrada: response.cerrada ?? false
    };
  }

  private defaultPeriod(): string {
    const date = new Date();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    return `${date.getFullYear()}-${month}`;
  }
}
