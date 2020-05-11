import React from 'react'
import MaterialTable from 'material-table';

const EU_columns = [
    {title:'Name', field:'name'},
    {title:'Type', field:'type'},
    {title:'Country', field:'country'},
    {title:'Phone', field:'phone'},
    {title:'E-mail', field:'email'},
    {title:'Number of EU Projects', field:'num'},
    {title:'Description', field:'description'}
]

const B2Match_columns = [
    {title:'Name', field:'name'},
    {title:'Org. Name', field:'org'},
    {title:'Type', field:'type'},
    {title:'Country', field:'country'},
    {title:'Website', field:'web'},
    {title:'Event Name', field:'event'},
    {title:'Description', field:'description'}
]

function SearchResults(props)
{
    const [data, setData] = React.useState([]);
    if (data.length === 0)
        setData(props.data);
    return (
        <React.Fragment>
            
        <div>
            {data.length === 0 ? null :
                <MaterialTable
                title="EU Funding and Tenders Portal Results"
                options={{exportButton:true}}
                columns={EU_columns}
                data={data}
                />}
        </div>
        <div style={{'margin-top' : '10px'}}>
            {data.length === 0 ? null :
                <MaterialTable
                title="B2MATCH Results"
                options={{exportButton:true}}
                columns={B2Match_columns}
                data={data}
                />}    
        </div>
        </React.Fragment>
      );
}
export default SearchResults;