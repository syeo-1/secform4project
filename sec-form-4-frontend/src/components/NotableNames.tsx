// info for the columns in the home page

// import { useEffect, useState } from "react";
// import { Transaction } from './types';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }

export default function NotableNames({data_list, title}: { data_list: string[], title: string}) {

    const data_list_li = data_list.map((data_item: string, index: number) => <li key={index}>{data_item}</li>);

    return (
        <>
            <h2>{title}</h2>
            <ol>
                {data_list_li}
            </ol>
        </>
    )
}