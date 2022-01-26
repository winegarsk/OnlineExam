//import * as Auth0 from 'auth0-web';
import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Exam} from './exam.model';
import {ExamsApiService} from './exams-api.service';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'exams',
  template: `
    <div>
      <button routerLink="/new-exam">New Exam</button>
      <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
        <button (click)="auth.logout({ returnTo: document.location.origin })">
          Log out
        </button>
      </ng-container>

      <ng-template #loggedOut>
        <button (click)="auth.loginWithRedirect({
          redirect_uri: 'http://localhost:4200/'
        })">Log in</button>
      </ng-template>
      
      <ul>
        <li *ngFor="let exam of examsList">
          {{exam.title}}
        </li>
      </ul>
    </div>
  `
})

//<button (click)="signIn()" *ngIf="!authenticated">Sign In</button>
//<button (click)="signOut()" *ngIf="authenticated">Sign Out</button>
//<p *ngIf="authenticated">Hello, {{getProfile!().name!}}</p>
export class ExamsComponent implements OnInit, OnDestroy {
  examsListSubs!: Subscription|undefined;
  examsList: Exam[]|undefined;
  authenticated = false;

  constructor(private examsApi: ExamsApiService, @Inject(DOCUMENT) public document: Document, public auth: AuthService) { }

  //signIn = Auth0.signIn;
  //signOut = Auth0.signOut;
  //getProfile = Auth0.getProfile;

  ngOnInit() {
    this.examsListSubs = this.examsApi
      .getExams()
      .subscribe(res => {
          this.examsList = res;
        },
        console.error
      );
    const self = this;
   // Auth0.subscribe((authenticated) => (self.authenticated = authenticated));
  }

  ngOnDestroy() {
    this.examsListSubs!.unsubscribe();
  }
}