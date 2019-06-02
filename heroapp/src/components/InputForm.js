import * as React from 'react';
import axios from 'axios';
import { config } from '../config';

class InputForm extends React.Component {
  state = {
    clientTask: null,
    heroNum: null,
    weekNum: null,
    dayPerWeek: null,
    weekdayHours: null
  };

  submitForm = () => {
    if (
      !!this.state.clientTask &&
      !!this.state.heroNum &&
      !!this.state.weekNum &&
      !!this.state.dayPerWeek &&
      !!this.state.weekdayHours
    ) {
      axios.post(`${config.serverUrl}/heroform`, { ...this.state }).then(({ status, data }) => {
        if (status >= 200 && status < 400) {
          this.props.history.push('display', data);
        } else {
          alert('Error: ' + status);
        }
      });
    } else {
      alert('Input invalid');
    }
  };

  onInputChange = e => {
    if (e.target && e.target.id) {
      switch (e.target.id) {
        case 'clientTask': {
          try {
            const trylist = JSON.parse(e.target.value);
            if (Array.isArray(trylist)) {
              this.setState({ clientTask: trylist });
            }
          } catch (e) {
            this.setState({ clientTask: null });
          }

          break;
        }
        case 'heroNum':
          this.setState({ heroNum: e.target.value });
          break;
        case 'weekNum':
          this.setState({ weekNum: e.target.value });
          break;
        case 'dayPerWeek':
          this.setState({ dayPerWeek: e.target.value });
          break;
        case 'weekdayHours':
          this.setState({ weekdayHours: e.target.value });
          break;
        default:
      }
    }
  };

  render() {
    return (
      <>
        <div className="container">
          <div className="row">
            <div className="col-md-8">
              <form>
                <div>
                  <label htmlFor="clientTask">Client Task</label>
                  <input
                    type="text"
                    className="form-control"
                    id="clientTask"
                    placeholder="Client Task List"
                    onInput={this.onInputChange}
                  />
                </div>
                <div>
                  <label htmlFor="heroNum">Hero number</label>
                  <input
                    type="text"
                    className="form-control"
                    id="heroNum"
                    placeholder="hero number"
                    onInput={this.onInputChange}
                  />
                </div>
                <div>
                  <label htmlFor="weekNum">Week Num</label>
                  <input
                    type="text"
                    className="form-control"
                    id="weekNum"
                    placeholder="Week Number"
                    onInput={this.onInputChange}
                  />
                </div>

                <div>
                  <label htmlFor="dayPerWeek">Days per Week</label>
                  <input
                    type="text"
                    className="form-control"
                    id="dayPerWeek"
                    placeholder="Days per Week"
                    onInput={this.onInputChange}
                  />
                </div>
                <div>
                  <label htmlFor="weekdayHours">Weekday hours</label>
                  <input
                    type="text"
                    className="form-control"
                    id="weekdayHours"
                    placeholder="Weekday hours"
                    onInput={this.onInputChange}
                  />
                </div>
              </form>
            </div>

            <div className="col-md-4" style={{ display: 'flex', alignItems: 'flex-end' }}>
              <div style={{ display: 'flex', flex: 1, justifyContent: 'center' }}>
                <button
                  onClick={this.submitForm}
                  type="button"
                  className="btn btn-primary"
                  style={{ paddingLeft: '20px', paddingRight: '20px' }}
                >
                  Go!
                </button>
              </div>
            </div>
          </div>
        </div>
        {/* <div>State: {JSON.stringify(this.state)}</div>
        <div>{JSON.stringify(!!this.state.clientTask)}</div>
        <div>{JSON.stringify(!!this.state.heroNum)}</div>
        <div>{JSON.stringify(!!this.state.weekNum)}</div>
        <div>{JSON.stringify(!!this.state.dayPerWeek)}</div>
        <div>{JSON.stringify(!!this.state.weekdayHours)}</div> */}
      </>
    );
  }
}

export default InputForm;
