import React, {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {FrontendUrl, historyStore, VkAppClientId} from "../../api/config";
import {Route} from "react-router-dom";
import {jwtController} from "../../api/Container/apiDI";

enum RoutesLogin{
    signIn = "/signin",
    apply = "/signin/apply",
    error = "/signin/error",
}

function LoginPageError() {
    return (
        <div>
            <h2>Авторизация прошла неуспешно</h2>
        </div>
    );
}

const LoginApplyPage = () => {
    const navigate = useNavigate();
    const payload = async () => {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        if ("code" in params && typeof params.code === "string" && params.code.length > 0) {
            try {
                await jwtController.accessByCode(params.code)
                console.log("Access token is giving");
                return;
            } catch (e){}
        }
        navigate( RoutesLogin.error)
    }
    // ignore payload... UseCookiesChangeable
    useEffect(() => {payload()}, []);
    return (
        <div>
            <h2>Авторизация...</h2>
        </div>
    );
}

function LoginPage() {
    function handle() {
        const apply = FrontendUrl + RoutesLogin.apply;
        const vkOauthUrl = `https://oauth.vk.com/authorize?client_id=${VkAppClientId}&redirect_uri=${apply}`
        historyStore.push(vkOauthUrl);
    }

    return (
        <div>
            <h2>User Account Center</h2>
            <button onClick={handle}>Login</button>
        </div>
    );
}

export function LoginRoute(): JSX.Element[] {
    return [
        <Route key={0} path={RoutesLogin.signIn} element={<LoginPage/>}/>,
        <Route key={1} path={RoutesLogin.apply} element={<LoginApplyPage/>}/>,
        <Route key={2} path={RoutesLogin.error} element={<LoginPageError/>}/>
    ];
}
