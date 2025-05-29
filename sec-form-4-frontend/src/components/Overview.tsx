// give info about bigges gainers/losers of the day
// plus also info about notable insiders worth tracking
// eg. Elon, Bezos, Zucc, Buffet, Jensen (nvidia) etc...
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import OverviewCardInfo from './OverviewCardnfo';
import NotableNames from './NotableNames';
import { Transaction } from './types';


export default function Overview() {

    return (
        <>
            <Grid container>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo homepage_text_css="homepage-text" homepage_title_css="homepage-overview-info-title" title="Top Sale Filing Data" transaction_type="S"/>
                </Grid>
                <Grid size={{ xs: 12, md: 4}}>
                    <OverviewCardInfo homepage_text_css="homepage-text" homepage_title_css="homepage-overview-info-title" title="Top Purchase Filing Data" transaction_type="P"/>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <OverviewCardInfo homepage_text_css="homepage-text" homepage_title_css="homepage-overview-info-title" title="Top Activity Stock Ticker"/>
                </Grid>
            </Grid>
        </>
    )
}