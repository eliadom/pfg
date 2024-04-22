import { ComponentFixture, TestBed } from '@angular/core/testing';
import {ModelsPassatsComponent} from "./models-passats.component";



describe('TaulaPrediccionsComponent', () => {
  let component: ModelsPassatsComponent;
  let fixture: ComponentFixture<ModelsPassatsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModelsPassatsComponent]
    });
    fixture = TestBed.createComponent(ModelsPassatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
