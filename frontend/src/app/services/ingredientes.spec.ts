import { TestBed } from '@angular/core/testing';

import { Ingredientes } from './ingredientes';

describe('Ingredientes', () => {
  let service: Ingredientes;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Ingredientes);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
