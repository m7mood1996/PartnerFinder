import React from 'react'
import MaterialTable from 'material-table';

const EU_columns = [
    { title: 'Name', field: 'legalName' },
    { title: 'Type', field: 'classificationType' },
    { title: 'Country', field: 'country' },
    { title: 'Data Status', field: 'dataStatus' },
    { title: 'Number of EU Projects', field: 'numberOfProjects' },
    { title: 'Description', field: 'description' },
    { title: 'Consorsium Role', field: 'consorsiumRoles' }
]

const B2Match_columns = [
    { title: 'Name', field: 'name' },
    { title: 'Org. Name', field: 'org' },
    { title: 'Type', field: 'type' },
    { title: 'Country', field: 'country' },
    { title: 'Website', field: 'web' },
    { title: 'Event Name', field: 'event' },
    { title: 'Description', field: 'description' }
]

const getRelativeData = (arr) => {
    let res = arr.map(org => {
        let temp = org
        let address = temp.address
        delete temp.pic
        delete temp.address
        temp = { ...temp, 'city': address.city, 'country': address.country }
        return temp
    })
    return res
}

function SearchResults(props) {
    const [data, setData] = React.useState([]);
    if (data.length === 0) {
        let tempData = props.data
        let eu = getRelativeData(tempData['EU'])
        tempData = { ...tempData, 'EU': eu }

        setData(tempData);
    }

    return (
        <React.Fragment>
            <div>
                {data.length === 0 ? null :
                    <MaterialTable
                        title="EU Funding and Tenders Portal Results"
                        options={{ exportButton: true }}
                        columns={EU_columns}
                        data={data.EU}
                    />}
            </div>
            <div style={{ 'margin-top': '10px' }}>
                {data.length === 0 ? null :
                    <MaterialTable
                        title="B2MATCH Results"
                        options={{ exportButton: true }}
                        columns={B2Match_columns}
                        data={data.B2MATCH}
                    />}
            </div>
        </React.Fragment>
    );
}
export default SearchResults;