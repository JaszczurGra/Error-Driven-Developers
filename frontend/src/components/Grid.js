import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useEffect } from "react";

export default function Grid({ data }) {
    return (
        <TableContainer component={Paper} sx={{ boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)", maxHeight: "800px" }}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table" stickyHeader>
                <TableHead>
                    <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>Action</TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                            Price
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                            Quantity
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                            Timestamp
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((row, index) => (
                        <TableRow
                            key={index}
                            sx={{
                                color: "black",
                                "&:last-child td, &:last-child th": { border: 0 },
                                backgroundColor: row.action === "Sell" ? "#24a800" : row.action === "Buy" ? "#a80000" : "inherit",
                                "&:hover": { opacity: 0.8 },
                            }}>
                            <TableCell component="th" scope="row">
                                {row.action}
                            </TableCell>
                            <TableCell align="right">{row.price}</TableCell>
                            <TableCell align="right">{row.quantity}</TableCell>
                            <TableCell align="right">{row.time}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
