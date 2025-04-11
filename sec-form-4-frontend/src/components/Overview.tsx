// give info about bigges gainers/losers of the day
// plus also info about notable insiders worth tracking
// eg. Elon, Bezos, Zucc, Buffet, Jensen (nvidia) etc...
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';

export default function Overview() {
    return (
        <>
            <Grid container>
                <Grid size={{ xs: 12, md: 4 }}>
                    <Paper>1</Paper>
                </Grid>
                <Grid size={{ xs: 12, md: 4}}>
                    <Paper>2</Paper>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <Paper>3</Paper>
                </Grid>
            </Grid>
        </>
    )
}