import SearchDetails from './search_details'
import React from 'react'
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

function MainScene() {

    return (
        <React.Fragment>
            <Container fixed>
                <Typography component="div" style={{ backgroundColor: '#cfe8fc', height: '100vh' }}>

                    <div>
                        <div className="Header">
                            <h1>Find Partner</h1>
                        </div>
                        <div>

                            <SearchDetails />
                        </div>
                    </div>
                </Typography>
            </Container>
        </React.Fragment>

    );
}
/*class MainScene extends Component {

    render(){
        return (
            <React.Fragment>
                <div>
                <h1>hey</h1>
                </div>
            </React.Fragment>

            
            
          );
        }
}*/

export default MainScene;

