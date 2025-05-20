// info for the columns in the home page

// import { useEffect, useState } from "react";
// import { Transaction } from './types';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }

export default function NotableNames({homepage_text_css, homepage_title_css, data_list, title}: { homepage_text_css: string, homepage_title_css: string, data_list: string[], title: string}) {

    const data_list_li = data_list.map((data_item: string, index: number) => <li key={index}>{data_item}</li>);

    return (
        <div className={homepage_text_css}>
            <h3 className={homepage_title_css}>{title}</h3>
            <ul>
                {data_list_li}
            </ul>
        </div>
    )
}