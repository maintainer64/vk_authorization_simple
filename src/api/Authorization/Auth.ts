import {IBasicAuth, IJWTTokenController, TJWTToken} from "./interface";
import {historyStore} from "../config";

export class AuthRepository implements IBasicAuth {
    private TIME_GAP = 20;
    protected accessToken?: TJWTToken;

    constructor(private jwt: IJWTTokenController, private readonly urlToAuth: string) {
    }

    protected isAccessTokenValid(): boolean {
        if (!this.accessToken) {
            return false;
        }
        return this.accessToken.exp - this.TIME_GAP > Date.now() / 1000;
    }

    async refreshToken():Promise<void> {
        try {
            this.accessToken = await this.jwt.refresh();
        } catch (e) {
            console.error("Token refresh failed");
            this.makeAuth();
        }
    }

    checkAuth(): Promise<void> {
        const isTokenValid = this.isAccessTokenValid();
        if (!isTokenValid) {
            return this.refreshToken();
        }
        return Promise.resolve();
    }

    makeAuth(): void {
        document.location.href = this.urlToAuth;
        historyStore.push(this.urlToAuth);
    }

    get tokenHeader(): string | null {
        if (this.accessToken){
            return `Bearer ${this.accessToken.token}`;
        }
        return null;
    }
}