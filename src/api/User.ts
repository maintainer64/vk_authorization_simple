import {createStore, createEffect, restore, combine, createEvent, forward} from 'effector'
import {IUser} from "./Clients/dto";
import {apiClientAuth} from "./Container/apiDI";



export const $UserAuthStore = createStore<IUser|null>(null);
export const setUserAuthStore = createEvent<IUser>();

const setUserAuthStoreFunc = (state: IUser|null, data: IUser) => {
    return data;
};
$UserAuthStore.on(setUserAuthStore, setUserAuthStoreFunc)

export const getUsersFx = createEffect<void, IUser, Error>();
const $fetchError = restore<Error>(getUsersFx.failData, null);
export const $UserAuthStoreStatus = combine({
  loading: getUsersFx.pending,
  error: $fetchError,
  data: $UserAuthStore,
});

const getUsersApi = async (): Promise<IUser> => {
    const profile = await apiClientAuth.getUserProfile();
    setUserAuthStore(profile);
    return profile;
}

getUsersFx.use(getUsersApi);