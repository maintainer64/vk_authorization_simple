import Cookies from "js-cookie";
import {IJWTTokenController, TJWTToken, TJWTTokens} from "./interface";
import {BaseJsonRpcRequestClass} from "../index";

export class JwtControllerRepository implements IJWTTokenController {
    constructor(private client: BaseJsonRpcRequestClass) {
    }

    async refresh(): Promise<TJWTToken> {
        const refresh_token = Cookies.get("refresh_token") || ""
        const tokens = await this.client.makeCall<{ refresh_token: string }, TJWTTokens>(
            "access_by_refresh", {refresh_token}
        );
        if (tokens !== undefined) {
            this.setCookies(tokens);
            return tokens.access;
        }
        throw "Refresh error";
    }

    setCookies(tokens: TJWTTokens): void {
        const expires = new Date(tokens.refresh.exp * 1000);
        Cookies.set("refresh_token", tokens.refresh.token, {
            expires,
            path: "/",
        });
    }

    async accessByCode(code: string): Promise<TJWTToken> {
        const tokens = await this.client.makeCall<{ code: string }, TJWTTokens>("access_by_code", {code});
        if (tokens !== undefined) {
            this.setCookies(tokens);
            return tokens.access;
        }
        throw "Access error token";
    }
}