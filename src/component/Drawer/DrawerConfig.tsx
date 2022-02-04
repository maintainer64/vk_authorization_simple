import * as React from "react";
import HomeIcon from "@mui/icons-material/Home";
import ModeEditOutlineIcon from "@mui/icons-material/ModeEditOutline";
import InboxIcon from "@mui/icons-material/MoveToInbox";

export interface IDrawerElement {
    title: string;
    separate?: boolean;
    url: string;
    icon?: any;
}

export const DrawerConfig: IDrawerElement[] = [
    {title: "Главная", url: "/", icon: <HomeIcon/>},
    {title: "Предпросмотр", url: "/task-create", icon: <ModeEditOutlineIcon/>},
    {title: "Предпросмотр", url: "/task-create", icon: <InboxIcon/>},
];

export const DrawerConfigWidth = 210;