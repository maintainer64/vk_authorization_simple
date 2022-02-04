import * as React from "react";
import { Link } from "react-router-dom";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Toolbar from "@mui/material/Toolbar";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";

import "./Drawer.css";
import {DrawerConfig, DrawerConfigWidth} from "./DrawerConfig";


export function DrawerCustomElement(){
    const list = DrawerConfig.map(({title, url, icon}, index) => (
        <ListItem button key={index}>
            <Link to={url}>
                {icon ? <ListItemIcon>{icon}</ListItemIcon> : null}
                <ListItemText primary={title} />
            </Link>
        </ListItem>
    ));
    return (
        <div className={"drawerTools"}>
            <Toolbar />
            <Divider />
            {list}
        </div>
    )
}

interface IDrawerCustomBoxProps{
    container: any;
    mobileOpen?:boolean;
    handleDrawerToggle?: () => void;
    children?: React.ReactNode;
}

export function DrawerCustomBox(props: IDrawerCustomBoxProps){
    return <Box
        component="nav"
        sx={{ width: { sm: DrawerConfigWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
    >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
            container={props.container}
            variant="temporary"
            open={props.mobileOpen}
            onClose={props.handleDrawerToggle}
            ModalProps={{
                keepMounted: true, // Better open performance on mobile.
            }}
            sx={{
                display: { xs: 'block', sm: 'none' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DrawerConfigWidth },
            }}
        >
            {props.children}
        </Drawer>
        <Drawer
            variant="permanent"
            sx={{
                display: { xs: 'none', sm: 'block' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DrawerConfigWidth },
            }}
            open
        >
            {props.children}
        </Drawer>
    </Box>
}