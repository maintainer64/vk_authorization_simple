export interface IBasicAuth{
    checkAuth(): Promise<void>
    get tokenHeader(): string | null
    makeAuth(): void
}

export type TJWTToken = {
    exp: number;
    token: string;
};

export type TJWTTokens = {
  access: TJWTToken;
  refresh: TJWTToken;
};

export interface IJWTTokenController{
    refresh(): Promise<TJWTToken>
    setCookies(tokens: TJWTTokens): void
    accessByCode(code: string): Promise<TJWTToken>
}