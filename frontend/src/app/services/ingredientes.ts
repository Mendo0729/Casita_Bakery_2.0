import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Ingrediente {
  id: number;
  nombre: string;
  cantidad: number;
  unidad_medida: string;
  punto_reorden: number;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  status_code: number;
  timestamp: string;
  errors: unknown;
  data: T;
}

export interface IngredientesData {
  ingredientes: Ingrediente[];
  pagina: number;
  por_pagina: number;
  total_paginas: number;
  total_ingredientes: number;
}

export interface IngredientePayload {
  nombre: string;
  cantidad: number;
  unidad_medida: string;
  punto_reorden: number;
}

@Injectable({
  providedIn: 'root'
})
export class IngredientesService {
  private apiUrl = 'http://localhost:5000/inventario/api/';

  constructor(private http: HttpClient) {}

  obtenerIngredientes(pagina = 1, porPagina = 10, buscar = ''): Observable<ApiResponse<IngredientesData>> {
    let params = new HttpParams()
      .set('pagina', pagina)
      .set('por_pagina', porPagina);

    if (buscar.trim()) {
      params = params.set('buscar', buscar.trim());
    }

    return this.http.get<ApiResponse<IngredientesData>>(this.apiUrl, { params });
  }

  crearIngrediente(payload: IngredientePayload): Observable<ApiResponse<Ingrediente>> {
    return this.http.post<ApiResponse<Ingrediente>>(this.apiUrl, payload);
  }

  actualizarIngrediente(id: number, payload: Partial<IngredientePayload>): Observable<ApiResponse<Ingrediente>> {
    return this.http.put<ApiResponse<Ingrediente>>(`${this.apiUrl}${id}`, payload);
  }
}
