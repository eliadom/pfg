import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaulaPrediccionsComponent } from './taula-prediccions.component';

describe('TaulaPrediccionsComponent', () => {
  let component: TaulaPrediccionsComponent;
  let fixture: ComponentFixture<TaulaPrediccionsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TaulaPrediccionsComponent]
    });
    fixture = TestBed.createComponent(TaulaPrediccionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
