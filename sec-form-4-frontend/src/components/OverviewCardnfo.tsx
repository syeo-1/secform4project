// info for the columns in the home page

// import { useEffect, useState } from "react";
import { Transaction } from './types';
import BasicMenu from './BasicMenu';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }

export default function OverviewCardInfo({data_list, update_data, title}: { data_list: Transaction[], update_data: React.Dispatch<React.SetStateAction<Transaction[]>>, title: string}) {

    const data_list_li = data_list.map((data_item: Transaction, index: number) => <li key={index}>{data_item.reporting_owner_name}</li>);

    // const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    // const open = Boolean(anchorEl);
    // const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    //     setAnchorEl(event.currentTarget);
    // };
    // const handleClose = () => {
    //     setAnchorEl(null);
    // };

    return (
        <>
            <h2>{title}</h2>
            <BasicMenu options={['Day','Week', 'Month', 'Year']} update_data={update_data} initial_title='Day' />
            <BasicMenu options={['Person', 'Company']} update_data={update_data} initial_title='Person' />
            <ol>
                {data_list_li}
            </ol>
        </>
    )
}