import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Cliente {
  id: number;
  nombre: string;
  activo: boolean;
  fecha_registro: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  status_code: number;
  timestamp: string;
  errors: unknown;
  data: T;
}

export interface ClientesData {
  clientes: Cliente[];
  pagina: number;
  por_pagina: number;
  total_paginas: number;
  total_clientes: number;
}

@Injectable({
  providedIn: 'root'
})
export class ClientesService {
  private apiUrl = '/cliente/api/';

  constructor(private http: HttpClient) {}

  obtenerClientes(pagina = 1, porPagina = 10, buscar = ''): Observable<ApiResponse<ClientesData>> {
    let params = new HttpParams()
      .set('pagina', pagina)
      .set('por_pagina', porPagina);

    if (buscar.trim()) {
      params = params.set('buscar', buscar.trim());
    }

    return this.http.get<ApiResponse<ClientesData>>(this.apiUrl, { params });
  }

  crearCliente(nombre: string): Observable<ApiResponse<Cliente>> {
    return this.http.post<ApiResponse<Cliente>>(this.apiUrl, { nombre });
  }

  actualizarCliente(id: number, nombre: string): Observable<ApiResponse<Cliente>> {
    return this.http.put<ApiResponse<Cliente>>(`${this.apiUrl}${id}`, { nombre });
  }

  eliminarCliente(id: number): Observable<ApiResponse<{ id: number }>> {
    return this.http.delete<ApiResponse<{ id: number }>>(`${this.apiUrl}${id}`);
  }
}
