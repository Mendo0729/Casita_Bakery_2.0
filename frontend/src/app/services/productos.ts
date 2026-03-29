import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Producto {
  id: number;
  nombre: string;
  precio: number;
  descripcion?: string | null;
  activo: boolean;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  status_code: number;
  timestamp: string;
  errors: unknown;
  data: T;
}

export interface ProductosData {
  productos: Producto[];
  pagina: number;
  por_pagina: number;
  total_paginas: number;
  total_productos: number;
}

export interface ProductoPayload {
  nombre: string;
  precio: number;
  descripcion?: string;
  activo?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ProductosService {
  private apiUrl = 'http://localhost:5000/producto/api/';

  constructor(private http: HttpClient) {}

  obtenerProductos(pagina = 1, porPagina = 10, buscar = ''): Observable<ApiResponse<ProductosData>> {
    let params = new HttpParams()
      .set('pagina', pagina)
      .set('por_pagina', porPagina);

    if (buscar.trim()) {
      params = params.set('buscar', buscar.trim());
    }

    return this.http.get<ApiResponse<ProductosData>>(this.apiUrl, { params });
  }

  crearProducto(payload: ProductoPayload): Observable<ApiResponse<Producto>> {
    return this.http.post<ApiResponse<Producto>>(this.apiUrl, payload);
  }

  actualizarProducto(id: number, payload: ProductoPayload): Observable<ApiResponse<Producto>> {
    return this.http.put<ApiResponse<Producto>>(`${this.apiUrl}${id}`, payload);
  }

  eliminarProducto(id: number): Observable<ApiResponse<{ id: number }>> {
    return this.http.delete<ApiResponse<{ id: number }>>(`${this.apiUrl}${id}`);
  }
}
