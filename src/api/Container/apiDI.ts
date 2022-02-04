import {AuthRepository} from "../Authorization/Auth";
import {JwtControllerRepository} from "../Authorization/JwtController";
import {BaseJsonRpcRequestClass} from "../index";
import {NonAuthRepository} from "../Authorization/NonAuth";
import {ApiClientProfile} from "../Clients/ApiClient";

const BackendURL = "http://localhost:5001/api/v1/jsonrpc";
const RouteToAuth = "/signin";
const fakeAuthRepository = new NonAuthRepository();

const basicClientNoAuth = new BaseJsonRpcRequestClass(BackendURL, fakeAuthRepository);
export const jwtController = new JwtControllerRepository(basicClientNoAuth);

const authRepository = new AuthRepository(jwtController, RouteToAuth);
const basicClientAuth = new BaseJsonRpcRequestClass(BackendURL, authRepository);

export const apiClientAuth = new ApiClientProfile(basicClientAuth);


