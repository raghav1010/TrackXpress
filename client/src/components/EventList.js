import { useEffect, useState } from "react";
import JsonFormatter from 'react-json-formatter'

const EventList = () => {
    const jsonStyle = {
        propertyStyle: { color: 'red' },
        stringStyle: { color: 'green' },
        numberStyle: { color: 'darkorange' }
      }
  const [data, setData] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    (async function () {
       let response = await fetch('http://0.0.0.0:5050/api/get/events', {
      method: 'GET',
      headers: {
        accept: 'application/json',
      },
    });
    let d = await response.json();
    console.log(response, d);
    if ( d.error ) {
        setError(d.error.message);
    } else {
        setData(d.result.records);
    }
    })();
  }, []);

  return (
    <div className="event-list-wrapper">
      {error && (
        <div className="form__wrapper--heading">{error}</div>
      )}
      {data.length <= 0 && (
        <div className="form__wrapper--heading">No events found</div>
      )}
      {data.length > 0 && (
        <div>
          <div className="form__wrapper--heading">Events</div>
          <div className="event-list">
            {data.map((d,i) => {
              return (
                <div key={i} className="event-item"> {/* We should not use key prop but here we don't have any node changes */}
                  <div className="form-element">
                    <label>Name : </label>
                    <div>{d.name}</div>
                  </div>
                  <div className="form-element">
                    <label>Description : </label>
                    <div>{d.description}</div>
                  </div>
                  <div className="form-element">
                    <label>Rules : </label>
                    <div>
                      <JsonFormatter
                        json={d.property_details}
                        tabWith={3}
                        jsonStyle={jsonStyle}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default EventList;
