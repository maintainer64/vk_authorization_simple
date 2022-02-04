import {nanoid} from "nanoid";
import {IBasicAuth} from "./Authorization/interface";

export interface IJsonRpcResponse<R> {
    result?: R;
    error?: any;
}

export class IJsonRpcError extends Error {
    public body: any;

    constructor(body: any) {
        super();
        this.body = body;
    }
}

export class BaseJsonRpcRequestClass {
    constructor(private readonly url: string, private readonly auth: IBasicAuth) {
    }

    async makeCall<R, S>(
        method: string,
        requestData: R,
        headers?: HeadersInit,
    ): Promise<S | undefined> {
        try {
            await this.auth.checkAuth();
        } catch (e) {
            console.error(e);
            throw e;
        }

        console.log("headers", headers);

        const result = await fetch(this.url, {
            method: "POST",
            body: JSON.stringify({
                method: method,
                id: nanoid(),
                jsonrpc: "2.0",
                params: requestData || {}
            }),
            headers: {
                "Content-Type": "application/json",
                "x-request-id": nanoid(),
                ...(this.auth.tokenHeader && {
                    Authorization: this.auth.tokenHeader,
                }),
                ...headers,
            },
        });

        if (result.status === 401) {
            this.auth.makeAuth();
        }

        if (result.status === 200) {
            const responseJson: IJsonRpcResponse<S> = await result.json();

            // Содержит ключ "result" — успешный вызов
            if ("result" in responseJson) {
                return responseJson.result;
            } else if ("error" in responseJson) {
                console.error("Error occured while loading data");
                throw new IJsonRpcError(responseJson.error);
            }
        }
        throw new Error("network error");
    }
}
