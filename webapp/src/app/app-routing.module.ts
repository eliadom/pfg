import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {TaulaPrediccionsComponent} from "./taula-prediccions/taula-prediccions.component";
import {SettingsComponent} from "./settings/settings.component";
import {BrowserModule} from "@angular/platform-browser";

const routes: Routes = [
  { path: 'predict', component: TaulaPrediccionsComponent},
  { path: 'settings', component: SettingsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes),
    BrowserModule
  ],
  exports: [RouterModule,
  ]
})
export class AppRoutingModule { }
