
import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs';
import {Exam} from './exam.model';
import {ExamsApiService} from './exams-api.service';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';
import { Inject } from '@angular/core';

@Component({
  selector: 'exams',
  template: `
    <div>
      <ul *ngIf="auth.user$ | async as user">
        <li>{{ user.name }}</li>
        <li>{{ user.email }}</li>
      </ul>
      <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
        <button (click)="auth.logout({ returnTo: document.location.origin })">
          Log out
        </button>
      </ng-container>

      <ng-template #loggedOut>
        <button (click)="auth.loginWithRedirect()">Log in</button>
      </ng-template>
        <button routerLink="/new-exam">New Exam</button>
    </div>
  `
})
export class ExamsComponent implements OnInit, OnDestroy {
  examsListSubs!: Subscription|undefined;
  examsList: Exam[]|undefined;
  authenticated = false;

  
  constructor(@Inject(DOCUMENT) public document: Document, private examsApi: ExamsApiService,public auth: AuthService) { }
 

  ngOnInit() {
    this.examsListSubs = this.examsApi
      .getExams()
      .subscribe(res => {
          this.examsList = res;
        },
        console.error
      );
    const self = this;
  }

  ngOnDestroy() {
    this.examsListSubs!.unsubscribe();
  }
}