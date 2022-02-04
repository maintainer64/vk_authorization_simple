import * as React from 'react';
import {useEffect} from 'react';
import Menu from '@mui/material/Menu';
import Container from '@mui/material/Container';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuIcon from '@mui/icons-material/Menu';
import {Avatar, IconButton, Toolbar, Typography} from "@mui/material";
import {$UserAuthStoreStatus, getUsersFx} from "../../api/User";
import {useStore} from "effector-react";

const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

export interface IPropsContent {
    window: any;
    mobileOpen: boolean;
    handleDrawerToggle: () => void;
}

export interface IPropsContentContext {
    context: IPropsContent;
    children?: React.ReactNode;
    title?: string;
    avatarInfo?: boolean;
    navMenu?: boolean;
}

interface IPropsToolbarHeader {
    props: IPropsContentContext
}

const ResponsiveAppBar = ({props}: IPropsToolbarHeader) => {
    const {loading, error, data} = useStore($UserAuthStoreStatus);

    useEffect(() => {
        !data && getUsersFx();
    }, [data]);

    const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);

    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    return (
        <Container>
            <Toolbar disableGutters>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    edge="start"
                    onClick={props.context.handleDrawerToggle}
                    sx={{mr: 2, display: {sm: 'none'}}}
                >
                    <MenuIcon/>
                </IconButton>
                <Typography sx={{flexGrow: 1}} variant="h6" noWrap component="div">
                    Responsive drawer
                </Typography>
                <div>
                    <Tooltip title="Open settings">
                        <IconButton onClick={handleOpenUserMenu} sx={{p: 0}}>
                            {
                                (!loading && data) ? <Avatar alt="Remy Sharp" src={data.photo_200}/> :
                                    <AccountCircle/>
                            }
                        </IconButton>
                    </Tooltip>
                    <Typography variant="subtitle1" noWrap component="span">
                        {(!loading && data) ? `${data.first_name} ${data.last_name}` : ""}
                    </Typography>
                    <Menu
                        sx={{mt: '45px'}}
                        id="menu-appbar"
                        anchorEl={anchorElUser}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}
                        keepMounted
                        transformOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}
                        open={Boolean(anchorElUser)}
                        onClose={handleCloseUserMenu}
                    >
                        {settings.map((setting) => (
                            <MenuItem key={setting} onClick={handleCloseUserMenu}>
                                <Typography textAlign="center">{setting}</Typography>
                            </MenuItem>
                        ))}
                    </Menu>
                </div>
            </Toolbar>
        </Container>
    );
};
export default ResponsiveAppBar;
