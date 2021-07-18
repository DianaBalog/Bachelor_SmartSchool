import { React } from 'react';
import { InstitutionsContainer, InstitutionsTitle } from '../Institutions/InstitutionsElements';
import { DataGrid, GridToolbar } from '@material-ui/data-grid';
import { useDemoData } from '@material-ui/x-grid-data-generator';
import { Marginer } from '../marginer';


const SearchSubjects = () => {
    const { data } = useDemoData({
        dataSet: 'Commodity',
        rowLength: 100,
        maxColumns: 6,
      });

    return (
        <InstitutionsContainer>
            <InstitutionsTitle>Search Subjects</InstitutionsTitle>
            <Marginer direction="vertical" margin={50} />
            <div style={{ height: 600, width: '80%', background: '#fff'}}>
                <DataGrid
                    {...data}
                    components={{
                    Toolbar: GridToolbar,
                    }}
                />
            </div>

            
        </InstitutionsContainer>
    )
}

export default SearchSubjects;