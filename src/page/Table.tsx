import * as React from 'react';
import {Link} from "react-router-dom";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import ListAltIcon from '@mui/icons-material/ListAlt';

enum StatusTask{
    Done,
    Wrong,
}
interface TaskElement{
    id: string,
    name: string,
    status?: StatusTask | null,
    grade: number,
    dueDate : string
}

interface TaskElementViewProps{
    element: TaskElement
}
function createData(
    name: string,
    status: StatusTask | null,
    grade: number,
    dueDate: string,
): TaskElement{
    return { id: "1", name, status, grade, dueDate};
}

const rows = [
    createData('Frozen yoghurt', StatusTask.Done, 7, "s"),
    createData('Ice cream sandwich', null, 9.0, "kdldf"),
    createData('Eclair', StatusTask.Wrong, 16.0, "dsffd"),
    createData('Cupcake', null, 3.7, "kddfdffd"),
    createData('Gingerbread', null, 16.0, "kddfdffd"),
    createData('Frozen yoghurt', StatusTask.Done, 7, "s"),
    createData('Ice cream sandwich', null, 9.0, "kdldf"),
    createData('Eclair', StatusTask.Wrong, 16.0, "dsffd"),
    createData('Cupcake', null, 3.7, "kddfdffd"),
    createData('Gingerbread', null, 16.0, "kddfdffd"),
    createData('Frozen yoghurt', StatusTask.Done, 7, "s"),
    createData('Ice cream sandwich', null, 9.0, "kdldf"),
    createData('Eclair', StatusTask.Wrong, 16.0, "dsffd"),
    createData('Cupcake', null, 3.7, "kddfdffd"),
    createData('Gingerbread', null, 16.0, "kddfdffd"),
    createData('Frozen yoghurt', StatusTask.Done, 7, "s"),
    createData('Ice cream sandwich', null, 9.0, "kdldf"),
    createData('Eclair', StatusTask.Wrong, 16.0, "dsffd"),
    createData('Cupcake', null, 3.7, "kddfdffd"),
    createData('Gingerbread', null, 16.0, "kddfdffd"),
];

function TaskElementIcon({status}:{status: StatusTask | null | undefined}){
    if (status === StatusTask.Done){
        return <CheckCircleIcon fontSize={"large"} viewBox="0 0 36 24" color={"success"}/>
    }
    if (status === StatusTask.Wrong){
        return <ErrorIcon fontSize={"large"} viewBox="0 0 36 24" color={"error"}/>
    }
    return <ListAltIcon fontSize={"large"} viewBox="0 0 36 24" color={"disabled"}/>
}

function TaskElementStatusResolver(status: StatusTask | null | undefined): string{
    if (status === StatusTask.Done){
        return "Успешно"
    }
    if (status === StatusTask.Wrong){
        return "Не успешно"
    }
    return "-"
}

function TaskElementView({element}: TaskElementViewProps){
    return (
        <TableRow
            key={element.name}
            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
        >
            <TableCell component="th" scope="row">
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        flexDirection: 'row',
                        p: 1,
                        m: 1,
                        bgcolor: 'background.paper',
                    }}
                >
                    <TaskElementIcon status={element.status}/>
                    <Link style={{textDecoration: 'none'}} to={`/task/view/${element.id}`}>{element.name}</Link>
                </Box>
            </TableCell>
            <TableCell align="right">{TaskElementStatusResolver(element.status)}</TableCell>
            <TableCell align="right">{element.dueDate}</TableCell>
            <TableCell align="right">{element.status ? `${element.grade}%` : '-'}</TableCell>
        </TableRow>
    )
}

export default function BasicTable() {
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 100 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Название задачи</TableCell>
                        <TableCell align="right">Статус</TableCell>
                        <TableCell align="right">Выполнить до</TableCell>
                        <TableCell align="right">Оценка</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TaskElementView element={row}/>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}