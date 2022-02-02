import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { AuthModule } from '@auth0/auth0-angular';
import {AppComponent} from './app.component';
import {ExamsApiService} from './exams/exams-api.service';
import {ExamFormComponent} from './exams/exam-form.components';
import {RouterModule, Routes} from '@angular/router';
import {ExamsComponent} from './exams/exams.components';

// import * as Auth0 from 'auth0-web';
import {CallbackComponent} from './callback.component';



const appRoutes: Routes = [
  { path: 'new-exam', component: ExamFormComponent },
  { path: '', component: ExamsComponent },
  { path: 'callback', component: CallbackComponent },
];


@NgModule({
  declarations: [
    AppComponent,
    ExamFormComponent,
    ExamsComponent,
    CallbackComponent,

  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AuthModule.forRoot({
      domain: 'dev-4-frsuj0.us.auth0.com',
      clientId: 'kYsfByzSV4rxmTJSX6jmaQumLeJZVjoM'
    }),
   RouterModule.forRoot(
      appRoutes,
      ),
  ],
  providers: [ExamsApiService],
  bootstrap: [AppComponent]
})
export class AppModule {
 /* constructor() {
    Auth0.configure({
      domain: 'dev-dm6nugc4.us.auth0.com',
      audience: 'https://online-exam.digituz.com.br',
      clientID: 'OznIr8gSuGNtPCfvFUsqgOXU4gd4PKaD',
      redirectUri: 'http://localhost:4200/callback',
      scope: 'openid profile manage:exams'
    });
  } */
}