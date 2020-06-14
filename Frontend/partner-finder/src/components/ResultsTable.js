import React from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { styled } from "@material-ui/core/styles";

import { tableIcons } from "../utils";

const MyTablePagination = styled(TablePagination)((theme) => ({
  color: "white",
  fontSize: "16px",
}));

function ResultsTable(props) {
  const [data, setData] = React.useState(props.data);
  const [columns] = React.useState(props.columns);
  const [title] = React.useState(props.title);

  React.useEffect(
    function effectFunction() {
      setData(props.data);
    },
    [props.data]
  );

  const handleDelete = (oldData) => {
    let newData = [...data];
    newData.splice(newData.indexOf(oldData), 1);
    setData(newData);
  };

  return (
    <React.Fragment>
      <div>
        {data && data.length === 0 ? null : (
          <MaterialTable
            style={{ color: "white", backgroundColor: "#02203c" }}
            icons={tableIcons}
            title={title}
            components={{
              Pagination: (props) => <MyTablePagination {...props} />,
              Toolbar: (props) => (
                <div
                  style={{
                    backgroundColor: "#02203c",
                    color: "white",
                  }}
                >
                  <MTableToolbar {...props} />
                </div>
              ),
            }}
            options={{
              actionsCellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              cellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              headerStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              searchFieldStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              filterCellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              showEmptyDataSourceMessage: false,
              hideFilterIcons: true,
              header: true,
              exportButton: true,
              exportAllData: true,
            }}
            columns={columns}
            data={data}
            editable={{
              onRowDelete: (oldData) =>
                new Promise((resolve) => {
                  setTimeout(() => {
                    resolve();
                    handleDelete(oldData);
                  }, 600);
                }),
            }}
          />
        )}
      </div>
    </React.Fragment>
  );
}
export default ResultsTable;
