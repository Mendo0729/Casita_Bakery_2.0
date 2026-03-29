import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Producto } from './productos';

export interface PedidoDetalle {
  id: number;
  pedido_id: number;
  producto_id: number;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  producto: Producto | null;
}

export interface Pedido {
  id: number;
  cliente_id: number;
  fecha_pedido: string | null;
  fecha_entrega: string | null;
  estado: 'pendiente' | 'entregado' | 'cancelado';
  total: number | null;
  detalles: PedidoDetalle[];
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  status_code: number;
  timestamp: string;
  errors: unknown;
  data: T;
}

export interface PedidosData {
  pedidos: Pedido[];
  pagina: number;
  por_pagina: number;
  total_paginas: number;
  total_pedidos: number;
}

export interface PedidoLineaPayload {
  producto_id: number;
  cantidad: number;
}

export interface CrearPedidoPayload {
  cliente_id: number;
  fecha_entrega?: string | null;
  productos_seleccionados: PedidoLineaPayload[];
}

export interface ActualizarPedidoPayload {
  fecha_entrega?: string | null;
  estado?: 'pendiente' | 'entregado' | 'cancelado';
  productos_seleccionados?: PedidoLineaPayload[];
}

@Injectable({
  providedIn: 'root'
})
export class PedidosService {
  private apiUrl = 'http://localhost:5000/pedidos/api/';

  constructor(private http: HttpClient) {}

  obtenerPedidos(
    pagina = 1,
    porPagina = 10,
    cliente = '',
    estado = ''
  ): Observable<ApiResponse<PedidosData>> {
    let params = new HttpParams()
      .set('pagina', pagina)
      .set('por_pagina', porPagina);

    if (cliente.trim()) {
      params = params.set('cliente', cliente.trim());
    }

    if (estado.trim()) {
      params = params.set('estado', estado.trim());
    }

    return this.http.get<ApiResponse<PedidosData>>(this.apiUrl, { params });
  }

  crearPedido(payload: CrearPedidoPayload): Observable<ApiResponse<Pedido>> {
    return this.http.post<ApiResponse<Pedido>>(this.apiUrl, payload);
  }

  actualizarPedido(id: number, payload: ActualizarPedidoPayload): Observable<ApiResponse<Pedido>> {
    return this.http.put<ApiResponse<Pedido>>(`${this.apiUrl}${id}`, payload);
  }
}
