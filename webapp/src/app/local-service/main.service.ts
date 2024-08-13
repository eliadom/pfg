import {Injectable} from '@angular/core';
import {preloadAndParseTemplate} from "@angular/compiler-cli/src/ngtsc/annotations/component/src/resources";

@Injectable({
  providedIn: 'root'
})

export class LocalStorageService {

  setLastPrediction(prediccio: any) {
    let prediccioInfo: { data: any, dia: Date } = { data: null, dia: null}
    prediccioInfo.data = prediccio;
    prediccioInfo.dia = new Date();
    let prediccioInfoString = JSON.stringify(prediccioInfo);
    localStorage.setItem('prediccio', prediccioInfoString)
  }


  getLastPrediction(){
    let prediccioInfoString =  localStorage.getItem('prediccio');
    let prediccioInfo = JSON.parse(prediccioInfoString);
    return prediccioInfo;
  }

}
