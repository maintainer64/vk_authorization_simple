import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";

import Home from "./page/Home";
import {useStore} from 'effector-react';
import {LoginRoute} from "./page/Authorization/Login";
import {$UserAuthStore} from "./api/User";
import {IPropsContent} from "./component/AppBarViewer/AppBar";

function App() {
    // const user = useStore($UserAuthStore);
    const [mobileOpen, setMobileOpen] = React.useState(false);
    const context: IPropsContent = {
        window: undefined,
        mobileOpen: mobileOpen,
        handleDrawerToggle: () => {
            setMobileOpen(!mobileOpen);
        }
    }
    const loginRoutes = LoginRoute();
    return (
        <BrowserRouter>
          <Routes>
              {loginRoutes}
              <Route path="/" element={
                  <Home context={context}/>
              }/>
          </Routes>
        </BrowserRouter>
    );
}

export default App;
