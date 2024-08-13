import { ComponentFixture, TestBed } from '@angular/core/testing';
import {OptimitzacioComponent} from "./optimitzacio.component";



describe('OptimitzacioComponent', () => {
  let component: OptimitzacioComponent;
  let fixture: ComponentFixture<OptimitzacioComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OptimitzacioComponent]
    });
    fixture = TestBed.createComponent(OptimitzacioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
