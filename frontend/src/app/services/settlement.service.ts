import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { SettlementResponse, SettlementTemplate } from '../../models/settlement.model';

@Injectable({
  providedIn: 'root'
})
export class SettlementService {
  private templatesUrl = '/api/expensas/templates/';
  private liquidarUrl = '/api/liquidar/';

  constructor(private http: HttpClient) {}

  getTemplates(): Observable<SettlementTemplate[]> {
    return this.http.get<{ status: string; data: any[] }>(this.templatesUrl).pipe(
      map(response => (response.data || []).map(item => this.mapTemplate(item)))
    );
  }

  getTemplatesByConsortium(cuitConsorcio: string): Observable<SettlementTemplate[]> {
    return this.http
      .get<{ status: string; data: any[] }>(`${this.templatesUrl}consorcio/${cuitConsorcio}/`)
      .pipe(map(response => (response.data || []).map(item => this.mapTemplate(item))));
  }

  getTemplateById(templateId: number): Observable<SettlementTemplate | undefined> {
    return this.http
      .get<{ status: string; data: any }>(`${this.templatesUrl}${templateId}/`)
      .pipe(map(response => (response?.data ? this.mapTemplate(response.data) : undefined)));
  }

  createTemplate(payload: any): Observable<any> {
    return this.http.post(`${this.templatesUrl}crear/`, payload);
  }

  updateTemplate(templateId: number, payload: any): Observable<any> {
    return this.http.put(`${this.templatesUrl}${templateId}/actualizar/`, payload);
  }

  deleteTemplate(templateId: number): Observable<any> {
    return this.http.delete(`${this.templatesUrl}${templateId}/eliminar/`);
  }

  preview(payload: any): Observable<SettlementResponse> {
    return this.http.post<{ status: string; data: SettlementResponse }>(this.liquidarUrl, payload).pipe(
      map(response => response.data)
    );
  }

  closeSettlement(payload: any): Observable<SettlementResponse> {
    return this.http.post<{ status: string; data: SettlementResponse }>(this.liquidarUrl, {
      ...payload,
      cerrar: true
    }).pipe(map(response => response.data));
  }

  private mapTemplate(item: any): SettlementTemplate {
    return {
      id: Number(item.id ?? item.id_expensa_template ?? 0),
      consorcio: item.consorcio ?? item.cuit_consorcio ?? null,
      nombre: item.nombre ?? 'Template',
      version: Number(item.version ?? 1),
      activo: Boolean(item.activo ?? true),
      config: item.config ?? undefined
    } as SettlementTemplate;
  }
}
