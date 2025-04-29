// info for the columns in the home page

// import { useEffect, useState } from "react";
import { Transaction } from './types';

// interface OverviewPropData {
//     // fetch_data: () => Promise<(string | any[])[]>;
//     // data_list: (string | any[])[] | Promise<(string | any[])[]>;
//     data_list: Transaction[] | string[]
// }

export default function OverviewCardInfo({data_list}: { data_list: Transaction[]}) {

    // const [data_list, set_data_list] = useState<(string | any[])[]>([])
    // const [loading, set_loading] = useState(true);
    // const [resolvedData, setResolvedData] = useState<(string | any[])[] | null>(null);

    // useEffect(() => {
    //     async function resolvedData() {
    //         if (data_list instanceof Promise) {
    //             const result = await data_list;
    //             setResolvedData(result);
    //         } else {
    //             setResolvedData(data_list);
    //         }
    //     }

    //     resolvedData();
    // }, [data_list]);

    // useEffect(() => {
    //     (async () => {
    //         if (data_list instanceof Promise) {
    //             const result = await data_list;
    //             console.log("is a promise!")
    //             setResolvedData(result);
    //         } else {
    //             setResolvedData(data_list);
    //         }
    //     })();
    // }, [data_list]);

    // if (!resolvedData) {
    //     return <div>Loading Data...</div>
    // }

    // let data_list_li;

    // if an element in the data_list only has a single element, then for now it's a name list, so render as so
    // if (typeof data_list[0] === 'string') {
    //     data_list_li = data_list.map((data_item: string, index: number) => <li key={index}>{data_item}</li>);
    // } else {
    //     data_list_li = data_list.map((data_item: Transaction, index: number) => <li key={index}>{data_item.reporting_owner_name}</li>);
    // }
    const data_list_li = data_list.map((data_item: Transaction, index: number) => <li key={index}>{data_item.reporting_owner_name}</li>);

    // otherwise, it's transaction data, which should be rendered as such

    // console.log(data_list_li)

    return (
        <>
            <h2>Temporary Title</h2>
            <ol>
                {data_list_li}
            </ol>
        </>
    )
}