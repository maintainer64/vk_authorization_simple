import CssBaseline from "@mui/material/CssBaseline";
import AppBar from "@mui/material/AppBar";
import {DrawerCustomBox, DrawerCustomElement} from "./Drawer";
import {DrawerConfigWidth} from "./DrawerConfig";
import Box from "@mui/material/Box";
import * as React from "react";
import ResponsiveAppBar, {IPropsContentContext} from "../AppBarViewer/AppBar";

export function DrawerBox(props: IPropsContentContext) {
    return (
        <Box sx={{display: 'flex'}}>
            <CssBaseline/>
            <AppBar
                position="fixed"
                sx={{
                    width: {sm: `calc(100% - ${DrawerConfigWidth}px)`},
                    ml: {sm: `${DrawerConfigWidth}px`},
                    p: 0,
                    pr: 0
                }}
            >
                <ResponsiveAppBar props={props}/>
            </AppBar>
            {props.navMenu !== false && (
                <DrawerCustomBox container={props.context.window} mobileOpen={props.context.mobileOpen}
                                 handleDrawerToggle={props.context.handleDrawerToggle}>
                    <DrawerCustomElement/>
                </DrawerCustomBox>)
            }
            {props.children}
        </Box>
    );
}