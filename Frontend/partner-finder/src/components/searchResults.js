import React from 'react';
import MaterialTable from 'material-table';

const columns = [
  { title: 'Legal Name', field: 'legalName' },
  { title: 'Business Name', field: 'businessName' },
  { title: 'Type', field: 'classificationType' },
  { title: 'Country', field: 'country' },
  { title: 'City', field: 'city' },
  { title: 'Description', field: 'description' },

]

function SearchResults(props) {


  const [data, setData] = React.useState([]);
  if (data.length === 0)
    setData(props.data);

  return (
    <div>
      {data.length === 0 ? null :
        <MaterialTable
          title="Organizations Results"
          columns={columns}
          data={data}
        />}
    </div>

  );
}

export default SearchResults;
