import React from "react";
import ResultsTable from "./ResultsTable";
import { EU_columns, B2Match_columns } from "../utils";

function SearchResults(props) {
  const [data, setData] = React.useState([]);

  React.useEffect(
    function effectFunction() {
      setData(props.data);
    },
    [props.data]
  );

  return (
    <React.Fragment>
      <div>
        {data && data.length === 0 ? null : (
          <ResultsTable
            title={"EU Funding and Tenders Portal Results"}
            columns={EU_columns}
            data={data.EU}
          />
        )}
      </div>
      <div style={{ "margin-top": "10px" }}>
        {data && data.length === 0 ? null : (
          <ResultsTable
            title={"B2MATCH Results"}
            columns={B2Match_columns}
            data={data.B2MATCH}
          />
        )}
      </div>
    </React.Fragment>
  );
}
export default SearchResults;
