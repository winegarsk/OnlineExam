export class Exam {
    constructor(
      public title: string | undefined,
      public description: string | undefined,
      public _id?: number | undefined,
      public updatedAt?: Date | undefined,
      public createdAt?: Date | undefined,
      public lastUpdatedBy?: string | undefined
    ) {}
  }
  