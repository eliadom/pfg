import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {TaulaPrediccionsComponent} from "./taula-prediccions/taula-prediccions.component";
import {SettingsComponent} from "./settings/settings.component";
import {BrowserModule} from "@angular/platform-browser";
import {ModelsPassatsComponent} from "./passats/models-passats.component";
import {OptimitzacioComponent} from "./optimitzacio/optimitzacio.component";

const routes: Routes = [
  { path: 'optimize', component: OptimitzacioComponent},
  { path: 'predict', component: TaulaPrediccionsComponent},
  { path: 'settings', component: SettingsComponent},
  { path: 'models', component: ModelsPassatsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes),
    BrowserModule
  ],
  exports: [RouterModule,
  ]
})
export class AppRoutingModule { }
