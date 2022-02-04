/**
 * home page
 */
import * as React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import {DrawerBox} from "../component/Drawer/DrawerBox";
import {DrawerConfigWidth} from "../component/Drawer/DrawerConfig";
import BasicTable from "./Table";
import {IPropsContentContext} from "../component/AppBarViewer/AppBar";


function Content(){
    return <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${DrawerConfigWidth}px)` } }}
    >
        <Toolbar />
        <BasicTable/>
    </Box>
}


export default function Home(props: IPropsContentContext) {
    return (
        <DrawerBox context={props.context} title={"Главная"}>
            <Content/>
        </DrawerBox>
    );
}
