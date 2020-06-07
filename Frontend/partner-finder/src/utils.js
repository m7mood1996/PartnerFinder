const EU_columns = [
    { title: "Name", field: "legalName" },
    { title: "Type", field: "classificationType" },
    { title: "Country", field: "country" },
    { title: "Data Status", field: "dataStatus" },
    { title: "Number of EU Projects", field: "numberOfProjects" },
    { title: "Description", field: "description" },
    { title: "Consorsium Role", field: "consorsiumRoles" },
];

const B2Match_columns = [
    { title: "Name", field: "participant_name" },
    { title: "Org. Name", field: "organization_name" },
    { title: "Type", field: "org_type" },
    { title: "Country", field: "address" },
    { title: "Website", field: "org_url" },
    { title: "Description", field: "description" },
];

const companyTypesOptions = [
    "SME",
    "International Organization",
    "Higher or Secondary Education",
    "Research Organization",
    "Private for Profit Organization",
    "Public Organization",
    "Other",
];

export { EU_columns, B2Match_columns, companyTypesOptions }