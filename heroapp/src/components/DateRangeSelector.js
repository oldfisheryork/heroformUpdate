import React, { Component } from "react";
import { DateRangePicker } from "react-dates";
import moment from "moment";

export default class DateRangeSelector extends Component {
  state = {
    startDate: moment().subtract(2, "year"),
    endDate: moment(),
    focusedInput: null
  };

  handleDateChange = ({ startDate, endDate }) =>
    this.setState({ startDate, endDate });

  handleFocusChange = focusedInput => this.setState({ focusedInput });

  isOutsideRange = () => false;

  render = () => (
    <DateRangePicker
       startDate={this.state.startDate}
       startDateId="startDate"
       endDate={this.state.endDate}
       endDateId="endDate"

       onDatesChange={this.handleDateChange}

       focusedInput={this.state.focusedInput}

       isOutsideRange={this.isOutsideRange}
       onFocusChange={this.handleFocusChange}

    />
  );
}

