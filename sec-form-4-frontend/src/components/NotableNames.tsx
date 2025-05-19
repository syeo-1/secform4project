// info for the columns in the home page

// import { useEffect, useState } from "react";
// import { Transaction } from './types';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }

export default function NotableNames({className, data_list, title}: { className: string, data_list: string[], title: string}) {

    const data_list_li = data_list.map((data_item: string, index: number) => <li key={index}>{data_item}</li>);

    return (
        <div className={className}>
            <h2>{title}</h2>
            <ul>
                {data_list_li}
            </ul>
        </div>
    )
}