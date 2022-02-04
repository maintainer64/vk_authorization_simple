import {BaseJsonRpcRequestClass} from "../index";
import { IUser } from "./dto";


export class ApiClientProfile{
    constructor(private client: BaseJsonRpcRequestClass) {}

    async getUserProfile(): Promise<IUser> {
        const profile = await this.client.makeCall<null, IUser>("profile_get", null);
        if (profile !== undefined){
            return profile;
        }
        throw "Profile not loaded";
    }
}