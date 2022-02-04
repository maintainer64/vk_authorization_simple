import {IBasicAuth} from "./interface";

export class NonAuthRepository implements IBasicAuth{
    checkAuth(): Promise<void> {
        return Promise.resolve();
    }
    makeAuth(): void {}

    get tokenHeader(): string | null {
        return null;
    }
}